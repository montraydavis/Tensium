# Tensium
Use Selenium and Machine Learning / Reinforcement Learning to figure out how to navigate a website.

![Tensium In Action](https://github.com/montraydavis/Tensium/blob/main/Tensium-src/content/001.gif?raw=true)

# Why Tensium?

The aim of this project is to automate the automation process. Currently, while website testing can be efficiently tested using various automation tools, the writing of such tests can be difficult and time consuming. Tensiums' goal is to simplify this manual coding process to some simple inputs.

Let's automate the automation process using Artificial Intelligence. Tensium learns how to navigate your webpage. Additionally, Tensium can execute a chain of API's and figure out which values to pass forward.

Use the botebook to get started with an example / tutorial, or use the python code to start building test cases.
In the src folder, you will find a [Jupyter Notebook](https://github.com/montraydavis/Tensium/blob/main/Tensium-src/notebook.ipynb) which breaks down the process.

# Tensium API Walker

Tensium API Walker allows Automation Engineers to build complex yet easily maintanable automated API tests.

This library makes it easy to quickly write automated API tests which require little to no maintenance (when using forward-feeding).

## How it works

Given a list of endpoints, and their possible inputs, Tensium will figure out how to exeute an API endpoint.

When chaining API calls, Tensium will forward feed the possible values to the next endpoint in the chain.

# Dependencies

- Gym
- Stable Baselines 3
- Numpy
- Selenium
- Matplotlib

## Artificial Intelligence

- Utilizes Artificial Intelligence
  - Q-Learning

## Selenium Support
- Selenium Command Wrappers
  - Set Input Values
  - Click Element
  - (More coming soon)
- Selenium
  - Full Selenium Support

## TestCases
- Easily and quickly create separated test cases with an individual learning model.

## Log

v.0.0.1:

Initial release.

- Basic training
- Selenium Command Wrappers

v.0.0.2:

- TestCase support.
  - Create individual testcases driven by TensiumEnv.
- Minor fixes
- Notebook update

v.0.1.0:
- Added Image Comparer (Tensorflow)
 - Compare previous screenshot to current screenshot noting differences with Tensorflow.
- API test support
 - Build automated API tests.