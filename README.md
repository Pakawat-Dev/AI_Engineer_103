# AI_Engineer_103 - Agent-to-Agent Protocol (A2A) with LangGraph and OpenAI Model

Automated tool that performs automated root cause analysis using the Fishbone Diagram method (also known as Ishikawa Diagram). This tool uses AI agents to identify causes and analyze root causes for any problem you describe.

## What is Fishbone Analysis?

Fishbone analysis is a problem-solving technique that helps identify potential causes of a problem by organizing them into categories. It's called "fishbone" because the diagram looks like a fish skeleton, with the problem at the head and causes branching out like bones.

## Features

- **AI-Powered Analysis**: Uses OpenAI's GPT models to identify causes and root causes
- **Multi-Agent System**: Three specialized agents work together:
  - Cause Identifier Agent: Finds initial causes in each category
  - Root Cause Analyzer Agent: Performs "5 Whys" analysis
  - Result Formatter Agent: Organizes and formats results
- **6M Categories**: Analyzes problems using the standard 6M framework:
  - Man (People)
  - Machine
  - Method
  - Material
  - Measurement
  - Environment
- **Interactive Interface**: Easy-to-use command-line interface
- **JSON Export**: Saves results for future reference

## Prerequisites

Before you start, make sure you have:

1. **Python 3.7 or higher** installed on your computer
2. **OpenAI API Key** (you'll need to sign up at [OpenAI](https://platform.openai.com/))

## Step-by-Step Installation Guide

### Step 1: Clone or Download the Project

If you have the files, make sure you have these files in your project folder:
- `fishbone.py`
- `requirements.txt`
- `.env` (you'll create this)

### Step 2: Set Up Python Virtual Environment (Recommended)

Open your terminal/command prompt and navigate to the project folder:

```bash
# Create a virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# Activate it (Mac/Linux)
source .venv/bin/activate
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- `python-dotenv`: For managing environment variables
- `langchain-openai`: For OpenAI integration
- `langgraph`: For agent workflow management

### Step 4: Set Up Your OpenAI API Key

1. Create a file named `.env` in your project folder
2. Add your OpenAI API key to the file:

```
OPENAI_API_KEY=your_api_key_here
```

**Important**: Replace `your_api_key_here` with your actual OpenAI API key.

## How to Use the Tool

### Step 1: Run the Program

```bash
python fishbone.py
```

### Step 2: Enter Your Problem

When prompted, describe the problem you want to analyze. For example:
- "Website is loading slowly"
- "Customer complaints are increasing"
- "Production quality is declining"

### Step 3: Review the Results

The tool will:
1. Identify potential causes in each of the 6M categories
2. Analyze root causes using the "5 Whys" technique
3. Display results in a tree format
4. Save results to a JSON file

### Example Output

```
================================================================================
FISHBONE ANALYSIS: Website is loading slowly
================================================================================

📁 Machine:
   ├── Server overload
   │   ├── Why? High traffic volume
   │   ├── Why? Insufficient server capacity
   │   └── Why? No load balancing

📁 Method:
   ├── Poor code optimization
   │   ├── Why? Inefficient database queries
   │   └── Why? Large image files
```

## Understanding the Results

- **📁 Categories**: The 6M categories (Man, Machine, Method, etc.)
- **├── Causes**: Potential causes identified in each category
- **└── Why?**: Root causes discovered through "5 Whys" analysis

## File Structure

```
project-folder/
├── fishbone.py              # Main program file
├── requirements.txt         # Python dependencies
├── .env                    # Your API key (create this)
├── .venv/                  # Virtual environment (created by you)
└── fishbone_analysis_*.json # Results files (created automatically)
```

## Troubleshooting

### Common Issues

**"Error: Please set OPENAI_API_KEY in your .env file"**
- Make sure you created the `.env` file
- Check that your API key is correct
- Ensure there are no extra spaces in the `.env` file

**"ModuleNotFoundError"**
- Make sure you activated your virtual environment
- Run `pip install -r requirements.txt` again

**"Connection Error"**
- Check your internet connection
- Verify your OpenAI API key is valid and has credits

### Getting Help

If you encounter issues:
1. Check that all files are in the correct location
2. Ensure your virtual environment is activated
3. Verify your OpenAI API key is working
4. Make sure you have an internet connection

## Tips for Better Results

1. **Be Specific**: Describe your problem clearly and specifically
2. **Use Business Language**: Avoid technical jargon when possible
3. **Focus on Observable Issues**: Describe what you can see or measure
4. **One Problem at a Time**: Analyze one main problem per session

## Example Problems to Try

- "Customers are waiting too long in line"
- "Email marketing campaigns have low open rates"
- "Manufacturing defects are increasing"
- "Employee turnover is high"
- "Software deployment takes too long"

## What's Next?

After running the analysis:
1. Review the identified causes and root causes
2. Prioritize which root causes to address first
3. Develop action plans to fix the most critical issues
4. Use the saved JSON files to track your analysis over time

## Advanced Usage

The tool saves detailed results in JSON format, including:
- Agent communication logs
- Timestamps
- Analysis metadata
- Complete cause hierarchy

You can use these files for further analysis or reporting.

---
