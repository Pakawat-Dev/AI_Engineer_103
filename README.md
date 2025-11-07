# AI_Engineer_103 

# Fishbone Analysis System 🐟

A beginner-friendly Python tool that uses AI to perform Fishbone Diagram analysis (also known as Cause-and-Effect or Ishikawa diagrams) to help identify root causes of problems.

## What is Fishbone Analysis?

Fishbone analysis is a problem-solving technique that helps you:
- Identify potential causes of a problem
- Organize causes into categories (like a fish skeleton)
- Find root causes using the "5 Whys" technique
- Visualize the relationship between problems and their causes

## What This Tool Does

This Python script uses OpenAI's GPT model to automatically:
1. **Analyze your problem** - Takes any problem you describe
2. **Find causes** - Identifies potential causes in 6 main categories (6M method)
3. **Dig deeper** - Uses "5 Whys" technique to find root causes
4. **Present results** - Shows organized, easy-to-read analysis
5. **Save results** - Exports analysis to JSON files

## Prerequisites (What You Need)

Before starting, make sure you have:
- Python 3.7 or higher installed on your computer
- An OpenAI API key (we'll show you how to get one)
- Basic command line knowledge (don't worry, we'll guide you!)

## Step-by-Step Setup Guide

### Step 1: Get Your OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up for an account (or log in if you have one)
3. Navigate to API Keys section
4. Click "Create new secret key"
5. Copy the key (it looks like: `sk-...`)
6. **Important**: Keep this key secret and safe!

### Step 2: Download the Project

1. Download all project files to a folder on your computer
2. Make sure you have these files:
   - `fishbone.py` (the main program)
   - `requirements.txt` (list of needed libraries)
   - `.env` (for your API key - we'll set this up)

### Step 3: Set Up Your Environment

#### Option A: Using Command Prompt (Windows)
```cmd
# Navigate to your project folder
cd path\to\your\fishbone\project

# Create a virtual environment (recommended)
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

#### Option B: Using Terminal (Mac/Linux)
```bash
# Navigate to your project folder
cd path/to/your/fishbone/project

# Create a virtual environment (recommended)
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 4: Configure Your API Key

1. Open the `.env` file in a text editor
2. Add your OpenAI API key like this:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
3. Replace `your_actual_api_key_here` with the key you copied from OpenAI
4. Save the file

**Example .env file:**
```
OPENAI_API_KEY=sk-1234567890abcdef1234567890abcdef
```

## How to Run the Program

### Step 1: Start the Program
```cmd
python fishbone.py
```

### Step 2: Enter Your Problem
When prompted, type the problem you want to analyze:
```
Enter problem to analyze (or 'quit' to exit): My website is loading slowly
```

### Step 3: Wait for Analysis
The program will:
- Show "Analyzing: Your problem"
- Display "Please wait..." while AI works
- This usually takes 10-30 seconds

### Step 4: Review Results
The program shows results organized by categories:
```
📁 Man (People):
   ├── Insufficient training
   │   └── Why? Limited onboarding process
   │   └── Why? No documentation standards

📁 Machine:
   ├── Server overload
   │   └── Why? High traffic volume
```

### Step 5: Check Saved Files
Results are automatically saved as JSON files with timestamps:
- `fishbone_analysis_20241106_143022.json`

## Understanding the Results

### The 6M Categories
The tool analyzes causes in these categories:
- **Man (People)**: Human-related causes (skills, training, etc.)
- **Machine**: Equipment, technology, hardware issues
- **Method**: Processes, procedures, workflows
- **Material**: Resources, inputs, supplies
- **Measurement**: Metrics, monitoring, data issues
- **Environment**: External factors, conditions

### Root Cause Analysis
For each cause, the tool asks "Why?" multiple times to find deeper root causes, helping you address the real problem, not just symptoms.

## Example Session

```
FISHBONE ANALYSIS SYSTEM
==================================================

Enter problem to analyze (or 'quit' to exit): Customer complaints increasing

🔄 Analyzing: Customer complaints increasing
⏳ Please wait...

================================================================================
FISHBONE ANALYSIS: Customer complaints increasing
================================================================================

📁 Man (People):
   ├── Untrained staff
   │   ├── Why? No formal training program
   │   └── Why? High employee turnover

📁 Method:
   ├── Poor complaint handling
   │   ├── Why? No standard procedures
   │   └── Why? Inconsistent response times

⏰ Completed at: 2024-11-06T14:30:22.123456
✅ Results saved to: fishbone_analysis_20241106_143022.json
```

## Troubleshooting Common Issues

### "Error: Please set OPENAI_API_KEY in your .env file"
- Check that your `.env` file exists
- Make sure the API key is correctly formatted
- Verify there are no extra spaces or quotes

### "Error initializing system"
- Check your internet connection
- Verify your OpenAI API key is valid
- Make sure you have credits in your OpenAI account

### "No causes identified"
- Try rephrasing your problem more specifically
- Check if your API key has sufficient credits
- Ensure your internet connection is stable

### Import Errors
- Make sure you activated your virtual environment
- Run `pip install -r requirements.txt` again
- Check that Python version is 3.7+

## Tips for Better Results

1. **Be Specific**: Instead of "system broken", try "login system fails after password reset"
2. **Use Clear Language**: Avoid jargon or overly technical terms
3. **One Problem at a Time**: Analyze separate issues individually
4. **Review Results**: The AI suggestions are starting points - use your expertise to validate

## What Each File Does

- **`fishbone.py`**: Main program with all the analysis logic
- **`requirements.txt`**: List of Python packages needed
- **`.env`**: Stores your OpenAI API key securely
- **`.venv/`**: Virtual environment folder (created when you set up)

## Cost Information

This tool uses OpenAI's API, which has costs:
- GPT-4o-mini model is very affordable
- Typical analysis costs less than $0.01
- Monitor usage in your OpenAI dashboard

## Getting Help

If you run into issues:
1. Check the troubleshooting section above
2. Make sure all steps were followed correctly
3. Verify your Python and pip installations
4. Check OpenAI API status and your account credits

## Advanced Usage

Once comfortable with basics, you can:
- Modify the categories in the code
- Adjust the number of causes per category
- Change the AI model used
- Customize the output format

## Next Steps

After running your first analysis:
1. Review the generated JSON files
2. Use insights to create action plans
3. Try analyzing different types of problems
4. Share results with your team for collaborative problem-solving
