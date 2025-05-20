# PCOS Care Agents

A multi-agent system for PCOS (Polycystic Ovary Syndrome) care and support, built using Microsoft's AutoGen framework.

## Features

- **PCOS Specialist**: Provides expert knowledge about PCOS symptoms, diagnosis, and treatment options.
- **Nutritionist**: Offers dietary advice and meal planning for PCOS management.
- **Fitness Coach**: Suggests exercise routines tailored for PCOS patients.

## Prerequisites

- Python 3.8+
- Google Gemini API key (for the LLM backend)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/pcos-care-agents.git
   cd pcos-care-agents
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Gemini API key:
   ```
   GOOGLE_GEMINI_API_KEY=your_api_key_here
   ```

## Usage

Run the main script to start interacting with the PCOS Care Agents:

```bash
python run_pcos_agents.py
```

Type your questions or concerns about PCOS, and the agents will work together to provide comprehensive support.

## Agents

### PCOS Specialist
- Provides medical information about PCOS
- Explains symptoms, causes, and treatments
- Offers guidance on managing PCOS symptoms

### Nutritionist
- Suggests PCOS-friendly diets
- Provides meal planning advice
- Recommends supplements and dietary changes

### Fitness Coach
- Creates exercise routines for PCOS management
- Suggests activities to improve insulin sensitivity
- Provides modifications for different fitness levels

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
