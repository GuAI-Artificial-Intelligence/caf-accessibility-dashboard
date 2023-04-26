# Web Application for Accessibility Analysis of Transportation

This application is part of the Consultancy for Hiring Web Application Implementation Services Focused on Transportation Accessibility Analysis as part of the "TUMI-DATA" Project, Data for Sustainable Mobility.

## Initial Requirements

Before you start using this project, please ensure that you have the following initial requirements:

- Python 3.9 installed: This project requires Python 3.9 or higher. If you don't have it installed, you can download it from the official Python website: [Python Website](https://www.python.org/downloads/)
- Pip 23.1 installed: Pip is the package installer for Python, and version 23.1 or higher is required for this project. If you don't have it installed, you can install it using the following command: `python -m ensurepip --default-pip`

## Installation

To get started with this project, follow the steps below:

1. Clone the repository to your local machine using the following command: `git clone <repository-url>`
2. Navigate to the project directory: `cd <repository-name>`
3. Install the required Python packages using Pip: `pip install -r requirements.txt`

## Usage

Once you have installed the required dependencies, you can start using the project. Follow the instructions below:

1. Run the main Python script: 
    * `python main.py` : to run the application in develop mode
    * `PROFILER="True" python main.py` : to run the application in profiler mode
    * `gunicorn wsgi:server --bind=0.0.0.0:8000` : to run de application in production mode
2. Follow the prompts or configure the project as needed
3. Enjoy the features of the project!

### Profiler mode
Allows the developer to visualize the performance characteristics of your Python code and identify potential bottlenecks or areas for optimization. To run the profiler mode, run the following commands: 
1. `PROFILER="True" python main.py`
2. `snakeviz profile`

## Contributing

If you would like to contribute to this project, please follow the guidelines below:

- Fork the repository
- Create a new branch for your contribution: `git checkout -b <branch-name>`
- Make your changes and test them thoroughly
- Commit your changes: `git commit -m "Your commit message here"`
- Push your changes to your forked repository: `git push origin <branch-name>`
- Create a pull request to the main repository with your changes

## License

This project is licensed under the MIT License license. Please see https://opensource.org/licenses/MIT for more information.

## Contact

If you have any questions, comments, or feedback, please feel free to contact us. You can reach us via email at info@guai.ai or by opening an issue in this repository.

Thank you for using the project! We hope you find it useful.