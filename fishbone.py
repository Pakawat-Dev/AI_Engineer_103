"""
Fishbone Diagram Root Cause Analysis with LangGraph.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

# Load environment variables
load_dotenv()

# Configuration constants
MODEL = "gpt-4o-mini"
MAX_CAUSES_PER_CATEGORY = 3
MAX_ROOT_CAUSES_PER_CAUSE = 3
CATEGORIES_6M = [
    "Man (People)",
    "Machine",
    "Method",
    "Material",
    "Measurement",
    "Environment"
]

class FishboneState(TypedDict):
    """State for Fishbone analysis workflow."""
    effect: str
    categories: List[str]
    causes: Dict[str, List[str]]
    root_causes: Dict[str, Dict[str, List[str]]]
    metadata: Dict[str, str]


class CauseIdentifierAgent:
    """Agent for identifying initial causes in Fishbone categories."""
    
    def __init__(self, model: str = MODEL, temperature: float = 0):
        self.agent_name = "cause_identifier"
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=800,
            timeout=30
        )
    
    def identify_causes(self, state: FishboneState) -> FishboneState:
        """Identify causes for each Fishbone category."""
        prompt = self._build_prompt(state["effect"], state["categories"])
        
        try:
            response = self.llm.invoke(prompt)
            data = self._parse_response(response.content)
            state["causes"] = self._extract_causes(data, state["categories"])
        except Exception as e:
            pass
            state["causes"] = {cat: [] for cat in state["categories"]}
        
        return state
    
    def _build_prompt(
        self,
        effect: str,
        categories: List[str]
    ) -> List[Dict[str, str]]:
        """Build prompt for cause identification."""
        return [
            {
                "role": "system",
                "content": (
                    f"You are a Root Cause Analysis expert. Return only JSON. "
                    f"Maximum {MAX_CAUSES_PER_CATEGORY} causes per category. "
                    f"Each cause should be 5 words or less."
                )
            },
            {
                "role": "user",
                "content": (
                    f'Effect: {effect}\n'
                    f'Categories: {", ".join(categories)}\n\n'
                    f'Return JSON format:\n'
                    f'{{"effect": "{effect}", '
                    f'"causes": {{"Category": ["cause1", "cause2", "cause3"]}}}}'
                )
            }
        ]
    
    def _parse_response(self, text: str) -> Dict:
        """Parse JSON response from LLM."""
        try:
            text = text.strip()
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            return json.loads(text)
        except (json.JSONDecodeError, IndexError):
            return {"causes": {}}
    
    def _extract_causes(
        self,
        data: Dict,
        categories: List[str]
    ) -> Dict[str, List[str]]:
        """Extract and validate causes from response."""
        causes = data.get("causes", {})
        result = {}
        
        for category in categories:
            category_causes = causes.get(category, [])
            if isinstance(category_causes, list):
                result[category] = [
                    c.strip() for c in category_causes 
                    if c and c.strip()
                ][:MAX_CAUSES_PER_CATEGORY]
            else:
                result[category] = []
        
        return result


class RootCauseAnalyzerAgent:
    """Agent for analyzing root causes using 5 Whys technique."""
    
    def __init__(self, model: str = MODEL, temperature: float = 0):
        self.agent_name = "root_cause_analyzer"
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=1000,
            timeout=30
        )
    
    def analyze_root_causes(self, state: FishboneState) -> FishboneState:
        """Analyze root causes for identified causes."""
        if not any(state["causes"].values()):
            state["root_causes"] = {}
            return state
        
        prompt = self._build_prompt(state["causes"])
        
        try:
            response = self.llm.invoke(prompt)
            data = self._parse_response(response.content)
            state["root_causes"] = self._organize_root_causes(
                data,
                state["causes"]
            )
        except Exception as e:
            pass
            state["root_causes"] = {}
        
        return state
    
    def _build_prompt(
        self,
        causes: Dict[str, List[str]]
    ) -> List[Dict[str, str]]:
        """Build prompt for root cause analysis."""
        cause_items = []
        for category, cause_list in causes.items():
            for cause in cause_list:
                cause_items.append(f'"{category}:{cause}"')
        
        return [
            {
                "role": "system",
                "content": (
                    f"Perform root cause analysis using 5 Whys. "
                    f"Return only JSON. {MAX_ROOT_CAUSES_PER_CAUSE} reasons per cause. "
                    f"Each reason should be 8 words or less."
                )
            },
            {
                "role": "user",
                "content": (
                    f'Analyze why these causes occur:\n'
                    f'[{", ".join(cause_items)}]\n\n'
                    f'Return JSON format:\n'
                    f'{{"Category:cause": ["why1", "why2", "why3"]}}'
                )
            }
        ]
    
    def _parse_response(self, text: str) -> Dict:
        """Parse JSON response from LLM."""
        try:
            text = text.strip()
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0].strip()
            elif '```' in text:
                text = text.split('```')[1].split('```')[0].strip()
            return json.loads(text)
        except (json.JSONDecodeError, IndexError):
            return {}
    
    def _organize_root_causes(
        self,
        data: Dict,
        causes: Dict[str, List[str]]
    ) -> Dict[str, Dict[str, List[str]]]:
        """Organize root causes by category and cause."""
        result = {}
        
        for category, cause_list in causes.items():
            result[category] = {}
            for cause in cause_list:
                key = f"{category}:{cause}"
                if key in data and isinstance(data[key], list):
                    result[category][cause] = [
                        rc.strip() for rc in data[key][:MAX_ROOT_CAUSES_PER_CAUSE]
                        if rc and rc.strip()
                    ]
                else:
                    result[category][cause] = []
        
        return result

class ResultFormatterAgent:
    """Agent for formatting and finalizing results."""
    
    def __init__(self, model: str = MODEL, temperature: float = 0):
        self.agent_name = "result_formatter"
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=1000,
            timeout=30
        )
    
    def format_results(self, state: FishboneState) -> FishboneState:
        """Add metadata and finalize results."""
        state["metadata"] = {
            "method": "Fishbone Diagram",
            "model": MODEL,
            "timestamp": datetime.now().isoformat(),
            "categories_analyzed": len(state["categories"]),
            "total_causes": sum(len(c) for c in state["causes"].values())
        }
        
        return state

class FishboneAnalyzer:
    """Orchestrator for the multi-agent Fishbone analysis."""
    
    def __init__(self):
        self.cause_identifier = CauseIdentifierAgent()
        self.root_analyzer = RootCauseAnalyzerAgent()
        self.result_formatter = ResultFormatterAgent()
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the agent workflow graph."""
        graph = StateGraph(FishboneState)
        
        # Register agent functions as nodes
        graph.add_node("identify_causes", self.cause_identifier.identify_causes)
        graph.add_node("analyze_roots", self.root_analyzer.analyze_root_causes)
        graph.add_node("format_results", self.result_formatter.format_results)
        
        # Define workflow sequence
        graph.set_entry_point("identify_causes")
        graph.add_edge("identify_causes", "analyze_roots")
        graph.add_edge("analyze_roots", "format_results")
        graph.add_edge("format_results", END)
        
        return graph.compile()
    
    def analyze(
        self,
        effect: str,
        categories: Optional[List[str]] = None
    ) -> Dict:
        """Execute the Fishbone analysis workflow."""
        if not effect.strip():
            raise ValueError("Effect cannot be empty")
        
        # Initialize state
        initial_state = FishboneState(
            effect=effect.strip(),
            categories=categories or CATEGORIES_6M.copy(),
            causes={},
            root_causes={},
            metadata={}
        )
        
        # Run workflow
        result = self.workflow.invoke(initial_state)
        
        # Extract relevant data for output
        return {
            "effect": result["effect"],
            "causes": result["causes"],
            "root_causes": result["root_causes"],
            "metadata": result["metadata"]
        }
    
    def display_results(self, results: Dict) -> None:
        """Display analysis results in formatted output."""
        print("\n" + "="*80)
        print(f"FISHBONE ANALYSIS: {results['effect']}")
        print("="*80)
        
        has_results = False
        for category, causes in results["causes"].items():
            if causes:
                has_results = True
                print(f"\n📁 {category}:")
                for cause in causes:
                    print(f"   ├── {cause}")
                    
                    # Show root causes
                    root_causes = results["root_causes"].get(category, {}).get(cause, [])
                    for i, rc in enumerate(root_causes):
                        if rc and rc != "Analysis pending":
                            connector = "└──" if i == len(root_causes) - 1 else "├──"
                            print(f"   │   {connector} Why? {rc}")
        
        if not has_results:
            print("\n❌ No causes identified. Please check your API key and try again.")
        
        print(f"\n⏰ Completed at: {results['metadata'].get('timestamp')}")
        print("-"*80)
    
    def save_results(self, results: Dict, filename: Optional[str] = None) -> None:
        """Save results to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fishbone_analysis_{timestamp}.json"
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to: {filename}")
        except IOError as e:
            print(f"❌ Error saving file: {e}")

def main():
    """Main entry point for interactive Fishbone analysis."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: Please set OPENAI_API_KEY in your .env file")
        sys.exit(1)
    
    print("\n" + "="*50)
    print("FISHBONE ANALYSIS SYSTEM")
    print("="*50)
    
    # Initialize analyzer
    try:
        analyzer = FishboneAnalyzer()
    except Exception as e:
        print(f"Error initializing system: {e}")
        sys.exit(1)
    
    analysis_count = 0
    
    # Interactive loop
    while True:
        effect = input("\nEnter problem to analyze (or 'quit' to exit): ").strip()
        
        if effect.lower() in ['quit', 'exit', 'q']:
            break
        
        if not effect:
            print("Please enter a valid problem statement.")
            continue
        
        try:
            print(f"\n🔄 Analyzing: {effect}")
            print("⏳ Please wait...")
            
            # Run analysis
            results = analyzer.analyze(effect)
            
            # Display and save results
            analyzer.display_results(results)
            analyzer.save_results(results)
            
            analysis_count += 1
            
        except KeyboardInterrupt:
            print("\n\nAnalysis interrupted.")
            break
        except Exception as e:
            print(f"Error during analysis: {e}")
            continue
    
    print(f"\n✅ Session completed. Analyses performed: {analysis_count}")
    print("Thank you for using the Fishbone Analysis System!")

if __name__ == "__main__":
    main()

