# 🌿 Production-Ready-LeafLogic-Multi-AI-Agents-Project  🌱  

# Problem Statement

***Note:** This project simulates an industry-standard scenario where we, a team of three contributors at XYZ Company, are developing an intelligent system capable of recognizing various plants and crops while providing users with accurate and detailed information about them. This system is designed to prevent misinformation and overpricing in the market by ensuring users can verify plant details instantly.*

## High-Level Note
Concepts related to AI agents, their pipelines, methodologies, and automated research processes have already been discussed. You can find these details in the *docs* folder for further exploration.

## 🌱 Building an Automated Plant and Crop Recognition System 🌿

At XYZ Company, we were tasked with developing a powerful AI-driven system that could recognize up to 100 different types of plants and crops while fetching complete details about them from the internet. The goal was to enable users to identify plants and obtain reliable information effortlessly, reducing the chances of misleading sales practices in the plant market.

### To achieve this, we leveraged a combination of:

- **Object Detection Models**: To accurately recognize various plant and crop species.
- **Multi-AI Agent Pipeline**: Handling detailed research on the detected plant/crop, covering scientific details, historical significance, health benefits, seasonal information, market price, and more.
- **OpenAI Model & UI Integration**: Generates a summary that is sent to the user via email.

## 🌿 Our Role as Developers 🌱

As a team of three contributors, our mission is to build a high-quality, scalable system that:

- Accurately detects a wide range of plants and crops.
- Automates the research process using multi-AI agents to gather real and accurate information from the internet.
- Ensures modular architecture for future scalability and easy maintenance.
- Provides users with trustworthy, well-structured insights on each recognized plant/crop.
- Maintains cost efficiency while delivering high performance and reliability.

This system is designed to deliver seamless plant identification and detailed research findings, ensuring that users have access to verified and comprehensive information. By integrating advanced Object Detection and AI Agents, we aim to create a reliable solution that empowers users with knowledge and prevents misinformation in the market.


## 🎯 Project Goals

### Deliver a System to Meet Client Needs

- Create a system to provide accurate and instant plant/crop insights, ensuring users receive reliable information.

### Build a Modular Architecture

- Design the system to support scalability and future upgrades, making modifications seamless.

### Testing and Quality Assurance

- Ensure the system’s reliability and accuracy through rigorous testing.

### Cost-Effective Measures

- Optimize API and model-related costs without compromising performance.

---

## ✨💚 Our Approach

The project followed a structured approach to ensure efficient execution and high-quality results.

### Steps in Our Approach

#### Framework Selection

- Chose **Object Detection with YOLOv5**, trained on an **A100 GPU** with a **self-annotated dataset** of **25K images**, which we later **open-sourced** for the community.
- For our AI Agents pipeline, we used taskflowai framework to build these (as it's high-quality open-source support framework-used to build Multi_AI Agent system).

#### Model Selection

- **OpenAI GPT-3.5 Turbo** was chosen for:
  - **Tool-Calling Excellence**: Best ability to call tools and manage multi-agent tasks seamlessly.
  - **Token Management**: Optimized context handling and reasoning.
  - **Report Generation**: Efficiently processing and generating structured reports.
- **LLaMA & Google Models** were tested but failed in reasoning, token management, and memory performance.
- **OpenAI o1 Series Models** offered strong performance but were too expensive for this project.
- **Groq Inference Engine** was also tested but did not meet the project’s performance indicators.

#### System Design and Development

- Built a **modular architecture**, ensuring future adaptability and easy upgrades.

#### Cost Optimization

- Minimized API costs by **choosing GPT-3.5 Turbo** and optimizing system performance.

#### Testing and Delivery

- Conducted rigorous testing to validate accuracy and reliability (in containers etc).
- Delivered the project on time, exceeding quality expectations.

---

## 🚧 Challenges Encountered

### 1. Model & API Cost

- Running inference and AI agents on cloud infrastructure was **cost-intensive**, requiring optimizations.

### 2. Training on a Large Dataset

- **Training on 25K images** with **A100 GPU** required substantial resources and time.

### 3. Cloud Inference Costs

- Running the **entire pipeline on the cloud** every time a user pings the system was expensive.

### 4. Data Annotation Process

- Annotation of **25K images** was a **time-consuming** and **labor-intensive** task, requiring collaboration among contributors.

## 🌟 How We Fixed Challenges  

#### Solutions Implemented

- **Choosing GPT-3.5 Turbo**: A cost-effective alternative while maintaining performance.  
- **Optimizing Training**: Trained the model on **100 epochs** with **25K images**, which was computationally intensive but proved effective.  
- **Cloud Cost Optimization**: Leveraged **EC2 instances** to fetch the **Docker image** from **ECR**, reducing overall cloud costs.  
- **Efficient Data Annotation**: Two contributors collaboratively annotated the dataset, significantly reducing annotation time and effort.  


---
## 🌿 System Design or Project Pipeline  

To simplify the complexity of our pipeline, we divide it into two main components:  

1. **Training Pipeline**  
2. **Prediction Pipeline + AI Agents**  

### 🔧 Training Pipeline  
  
*This is how **Training Pipeline** looks like*  

![CI_CD Diagram](https://github.com/user-attachments/assets/5e55752c-655e-401b-bd3a-628652c5b162)

First, we will retrieve data from **S3** as part of the **Data Ingestion Process** using this script.  


<img width="820" alt="s3_config" src="https://github.com/user-attachments/assets/2ec531d4-c595-4762-9e7f-53e7a69a33a0" />

- The `download_file` method:
  - Retrieves the file size using `head_object` for accurate progress tracking.
  - Uses `TransferConfig` to enable efficient multipart downloads (5MB chunks).
  - Implements a **progress callback** (`ProgressPercentage`) to log real-time updates.
  - Logs the start and completion of the download process for better visibility.
  - Handles errors gracefully by raising a `CustomException` on failure.

- The `run()` method 



















## License 📜  

This project is licensed under the **MIT License**.  
Feel free to use, modify, and share it with proper attribution. For more details, see the [LICENSE](LICENSE) file. 🌟  ....

