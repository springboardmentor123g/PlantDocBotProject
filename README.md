# PlantDocBotProject

## Description
This project contains Milestone1, Milestone2, Milestone3, and Milestone4 of the Plant Disease Detection Bot.  
It is designed to detect plant diseases using ML models and provides a frontend interface for users to interact with the system.

## Project Structure
- **Milestone1**: Initial setup and dataset exploration.
- **Milestone2**: Frontend and Backend integration.
- **Milestone3**: Improved model and UI enhancements.
- **Milestone4**: Final deployment-ready version with all features.

## Prerequisites
Before running the project, ensure you have the following installed:
- Python 3.10 or higher
- Git
- Git LFS (for large ML model files)
- Node.js and npm (for frontend)
- Required Python packages (`requirements.txt`)

## Setup Instructions

### 1. Clone the Repository

pip install -r requirements.txt

cd Milestone2/Frontend_server
npm install

git lfs install
git lfs pull

cd Milestone2/Frontend_server/Backend_server
python app.py

cd Milestone2/Frontend_server
npm start

git lfs track "*.safetensors"

git add Milestone5
git add .gitattributes

git commit -m "Add Milestone5 with ML model"

git push origin branch_name



