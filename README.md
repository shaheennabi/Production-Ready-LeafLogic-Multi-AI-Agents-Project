# 🌿 Production-Ready-LeafLogic-Multi-AI-Agents-Project  🌱  
*visitors: please wait for few seconds till readme loads (actually it's image heavy).*
# Problem Statement

***Note:** This project was assigned to us by **iNeuron Intelligence Pvt Ltd**, where our team of three contributors is developing an intelligent system capable of recognizing various plants and crops while providing users with accurate and detailed information about them. This system is designed to prevent misinformation and overpricing in the market by ensuring users can verify plant details instantly.*  


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

![CI_CD Diagram](https://github.com/user-attachments/assets/6edb279e-2b16-4c26-a478-d43e31d3dcb2)


First, we will retrieve data from **S3** as part of the **Data Ingestion Process** using this script from `utils`.  


<img width="820" alt="s3_config" src="https://github.com/user-attachments/assets/2ec531d4-c595-4762-9e7f-53e7a69a33a0" />

- The `download_file` method:
  - Retrieves the file size using `head_object` for accurate progress tracking.
  - Uses `TransferConfig` to enable efficient multipart downloads (5MB chunks).
  - Implements a **progress callback** (`ProgressPercentage`) to log real-time updates.
  - Logs the start and completion of the download process for better visibility.
  - Handles errors gracefully by raising a `CustomException` on failure.

- The `run()` method acts as an entry point to execute the download seamlessly

###  Data Ingestion

After downloading the dataset from **S3** as `leaflogic_dataset.zip`, it is stored in the **data_ingestion_dir**. The script then extracts the dataset into the **feature_store_path**, ensuring the data is properly organized for further processing.

*This is the shot of only `initiate_data_ingestion` for more go to `src/leaflogic/components/data_ingestion.py`
<img width="815" alt="Screenshot 2025-03-01 101319" src="https://github.com/user-attachments/assets/3a41a758-72b1-4f56-8a89-8e77b4faf17f" />


- **Initialization (`__init__` Method)**:  
  - Sets up the data ingestion directory.  
  - Logs initialization status.  

- **Data Download (`download_data` Method)**:  
  - Downloads the dataset from **S3** and saves it as `leaflogic_dataset.zip`.  
  - Uses **S3FileDownloader** to fetch the file.  

- **Data Extraction (`extract_zip_file` Method)**:  
  - Extracts `leaflogic_dataset.zip` into a temporary directory.  
  - Moves only the relevant dataset (`leaflogic_dataset`) into the **feature_store_path**.  
  - Cleans up temporary files after extraction.  

- **Data Ingestion Pipeline (`initiate_data_ingestion` Method)**:  
  - Calls the download and extraction methods in sequence.  
  - Returns a **DataIngestionArtifact**, storing paths to the downloaded and extracted dataset.  
  - Ensures proper logging and exception handling to track failures efficiently.  


### Prepare  BaseModel

After **data ingestion**, we prepare the base model by configuring `yolov5s.yaml` into `custom_yolov5s.yaml`. This involves updating the **number of categories (nc)** from `data.yaml` and defining essential parameters such as the **backbone, head, and other configurations** for training.

*This is the shot of only `prepare_basemodel` for more go to `src/leaflogic/components/prepare_base_model.py`
<img width="818" alt="Screenshot 2025-03-01 101223" src="https://github.com/user-attachments/assets/fa500189-bba4-4bc5-9a09-253a3f49af7f" />

- **Initialization (`__init__` Method)**:  
  - Loads the data ingestion artifacts.  
  - Locates `data.yaml` to retrieve the number of classes (`nc`).  
  - Ensures the file exists before proceeding.  

- **Updating Model Configuration (`update_model_config` Method)**:  
  - Reads `data.yaml` to extract the number of categories.  
  - Loads the base YOLOv5 model config (`yolov5s.yaml`).  
  - Updates the `nc` field along with other essential configurations.  
  - Saves the modified configuration as `custom_yolov5s.yaml`,  
    but for **preserving the original structure**, we have written a custom `write_yaml_file` function in `utils`.  
    When modifying the `nc` parameter, the default YAML formatting would break, so this function ensures the correct structure is maintained.
  
*these are the shots of `write_yaml_file` for maintaining structure from `utils`  
<img width="813" alt="wt" src="https://github.com/user-attachments/assets/ced94e0e-b236-4f3b-a0db-86ab8222b544" />
<img width="818" alt="wr1" src="https://github.com/user-attachments/assets/cea223d0-b84f-4ea5-abf0-ed9ea9272c84" />
<img width="812" alt="wr2" src="https://github.com/user-attachments/assets/184f09f6-db55-4b34-85f1-e11298f1d07e" />

*back to `prepare_basemodel`*
- **Model Preparation (`prepare_model` Method)**:  
  - Calls `update_model_config()` to generate the custom YOLOv5 config.  
  - Returns an artifact containing the path to the updated configuration file.  
  - Ensures all changes are logged for tracking and debugging. 

###  Model Trainer
After preparing the base model, we proceed to **training**. This stage utilizes the `data_ingestion` and `prepare_base_model` artifacts to train the model effectively.

  

*These are the shots of only `initiate_model_trainer` for more go to `src/leaflogic/components/model_training.py`
<img width="848" alt="mt" src="https://github.com/user-attachments/assets/04069879-a048-48e5-bc8e-5cfeca989738" />
<img width="806" alt="mt2" src="https://github.com/user-attachments/assets/eb6abdd5-f009-45b3-96f8-d980fb6660f1" />

During this stage:
- We **relocate** dataset files (`train`, `valid`, `test`, `data.yaml`) to the root directory to simplify file path management during training.  
- We **initiate the training** process using YOLOv5, specifying the dataset, model architecture, training parameters, and hardware configurations.  
- After training, we **move the best-trained model (`best.pt`)** to the root directory for easier access.  
- Finally, we **clean up unnecessary files** from the root directory to maintain a structured workspace. 

 *code overview* 
 
- **Initialization (`__init__` Method)**:  
  - Loads the **data ingestion** and **base model preparation** artifacts.  
  - Retrieves essential file paths such as `data.yaml`, the updated model config, and the model trainer directory.  
  - Ensures that `data.yaml` and the model config exist before proceeding.  

- **Moving Data for Training (`move_data_files_to_root` Method)**:  
  - Moves `data.yaml`, `train`, `valid`, and `test` directories from `feature_store_path` to the root directory.  
  - This ensures compatibility with the training script.  

- **Model Training (`initiate_model_trainer` Method)**:  
  - Moves data files to the root directory for ease of training.  
  - Runs the **YOLOv5 training script** with the correct configurations.  
  - Saves the **best model (`best.pt`)** to the root directory for easier access.  
  - Deletes unnecessary files (`data.yaml`, `train`, `valid`, `test`) after training is complete.  

- **Post-Training Cleanup (`delete_data_files_from_root` Method)**:  
  - Removes `data.yaml`, `train`, `valid`, and `test` directories from the root after training.  
  - Ensures a clean working environment.  

### ** and here the *training pipeline* ends **

---
### 🔍 Prediction Pipeline + AI Agents  

Now that we have successfully trained our model, let's move on to the **prediction pipeline** and **AI agents**. This phase involves using the trained model to detect objects in images and leveraging AI agents to fetch relevant insights about the detected crops/plants.  

### ** now let's talk about our Prediction Pipeline + AI Agents**

*This is how **Prediction Pipeline + AI Agents** looks like* 

![CI_CD Diagram (1)](https://github.com/user-attachments/assets/753c187e-e67f-4162-a4c3-e1a959a69113)

first let me take you to the tour of `app.py` that is present in `root directory` that orchestrates the object detection and AI research pipeline. It first defines necessary paths and functions to handle detection, processing, and research execution.

#### 1. Defining Paths and Functions  
Before executing the pipeline, the script defines essential paths and utility functions to manage object detection and research processing.

#### 2. Fetching the Latest Experiment Folder  
The function `get_latest_exp_folder()` retrieves the most recent experiment folder stored in `yolov5/runs/detect`. This ensures that the latest detection results are used in the pipeline.

#### 3. Running Object Detection  
To perform object detection, the script executes `run_yolo_detection()`, which utilizes the `os.system` command to run the YOLO model. The detected results are stored inside `detected_objects.txt`.

#### 4. Processing Predictions  
The detected indices are mapped to category labels using `process_prediction()`. This function relies on `get_label_by_idex` from `utils`, which compares each detected index with the categories defined in `data.yaml`.

#### 5. Reading Detected Objects  
The function `read_detected_objects()` reads the detected object labels from `detected_objects.txt`. These labels are then passed to AI agents for further analysis.

#### 6. Executing AI Research  
To gather insights on detected objects, `execute_research_and_report()` is invoked. This function triggers multiple research tasks:  
   - `research_overall_web` – General web research  
   - `research_health` – Health-related information  
   - `research_season` – Seasonal relevance  
   - `research_price` – Market price analysis  

#### 7. Saving and Summarizing Results  
The research findings are stored in `research_results`, and the `generate_summaried_report()` function compiles a final summarized report.

This structured approach ensures an efficient pipeline, from object detection to AI-powered analysis and reporting.

*almost every function in `app.py` is invoked by `/predict` route*, after all of it the report is sent to email -> user provides. 

### **Now, let's talk about each portion step-by-step**

You can explore `app.py` to see how functions like `get_latest_exp_folder()`, `run_yolo_detection()`, `process_prediction()`, and `read_detected_objects()` work. Additionally, also look at how `execute_research_and_report()` sequentially executes tasks and how `generate_summaried_report()` compiles the final report.  (not too difficult)

Since the README will become extensive, we'll focus on the key components and their underlying structure, such as:  **`research_overall_web`**, **`research_health`**, **`research_season`**, **`research_price`**.


### research_overall_web task

<img width="815" alt="research" src="https://github.com/user-attachments/assets/d9ed07f5-fa67-443d-addc-8ba95ef29824" />

1. **Agent Initialization**  
   - It initializes the `WebResearchAgent` using `WebResearchAgent.initialize_web_research_agent()`.  
   - This agent is designed to search the web and gather relevant information efficiently.  

2. **Task Creation**  
   - A `Task` object is created using `Task.create()`, where:  
     - The **agent** is assigned to perform the task.  
     - The **context** includes the plant’s name for reference.  
     - The **instruction** specifies details to be researched, such as:  
       - Scientific classification, origin, and regions.  
       - Uses, benefits, and growth conditions.  
       - Common pests, diseases, and economic significance.  
       - Fetching **relevant images** related to the plant.  



### research_health task

<img width="820" alt="health" src="https://github.com/user-attachments/assets/7376e5da-be33-4eba-be36-668ab106f74b" />

1. **Agent Initialization**  
   - The function initializes the `WebResearchAgent` using `WebResearchAgent.initialize_web_research_agent()`.  
   - This agent searches the web for reliable health-related information.  

2. **Task Creation**  
   - A `Task` object is created using `Task.create()`, where:  
     - The **agent** is assigned to perform the task.  
     - The **context** includes the plant’s name for better focus.  
     - The **instruction** outlines key health aspects to research:  
       - **Medicinal benefits** and traditional uses.  
       - **Potential risks** and toxicity concerns.  
       - **Nutritional value** and components.  
       - **Traditional remedies** where applicable.  
     - The gathered insights should be structured and referenced properly.


### research_season task

<img width="806" alt="season" src="https://github.com/user-attachments/assets/800e5bce-2d24-4706-a1c2-1da371e106d9" />

#### **How it Works**  
1. **Agent Initialization**  
   - The function initializes the `WebResearchAgent` using `WebResearchAgent.initialize_web_research_agent()`.  
   - This agent specializes in retrieving web-based agricultural knowledge.  

2. **Task Creation**  
   - A `Task` object is created via `Task.create()`, with:  
     - The **agent** assigned to perform the research.  
     - The **context** specifying the plant’s name for relevance.  
     - The **instruction** outlining key seasonal aspects to explore:  
       - **Planting & harvesting seasons** for optimal yield.  
       - **Climate conditions** including temperature and humidity.  
       - **Soil composition, nutrients, and fertilizers** best suited for growth.  
       - **Best farming practices** to maximize productivity.  
       - **Off-season storage & uses** to maintain quality and availability.  
     - The research must be backed by expert agricultural sources.  

### research_price task

<img width="815" alt="price" src="https://github.com/user-attachments/assets/7dd2ec86-a4f9-493e-af67-0675b2f97e0f" />

1. **Agent Initialization**  
   - The function initializes the `PriceFetchingAgent` using `PriceFetchingAgent.initialize_price_fetching_agent(query=plant_name)`.  
   - This agent specializes in fetching up-to-date pricing data from online sources.  

2. **Task Creation**  
   - A `Task` object is created via `Task.create()`, with:  
     - The **agent** assigned to fetch pricing data.  
     - The **context** specifying the plant’s name for relevance.  
     - The **instruction** detailing the required price-related insights:  
       - **Online price rates** across various marketplaces.  
       - **Cheapest price available** for the plant.  
       - **Identification of the lowest available price** and its source.  
     - The research must provide **accurate and current** market data.  


### **let's now see the `agents` these tasks use**

### web_research_agent

<img width="866" alt="web re" src="https://github.com/user-attachments/assets/c791d3f1-3623-4bbb-a17a-311633e1fdeb" />

The `WebResearchAgent` gathers key details about crops and plants using online sources.  

- **Agent Role & Goal**  
  - Acts as a **"Crop and Plant Research Agent"**, focused on collecting classification, uses, and growth data.  
  - Uses a structured, data-driven approach.  

- **LLM & Tools**  
  - Powered by `LoadModel.load_openai_model()`.  
  - Utilizes:  
    - `WikiArticles.fetch_articles` → Wikipedia data.  
    - `WikiImages.search_images` → Plant images.  
    - `ExaSearch.search_web` → Web-based insights.  

- **Error Handling**  
  - If initialization fails, an exception is raised.  

This agent ensures accurate and structured plant research.  

### price_fetching_agent

<img width="863" alt="price fe" src="https://github.com/user-attachments/assets/e80cef93-3ec7-4a63-8d76-f0d1da575d13" />

The `PriceFetchingAgent` helps find and compare the best prices for crops and plants across different markets.   

- **Agent Role & Goal**  
  - Acts as a **"Price Research Agent"**, specializing in market price analysis.  
  - Focuses on cost-conscious and data-driven price comparisons.  

- **LLM & Tools**  
  - Powered by `LoadModel.load_openai_model()`.  
  - Utilizes:  
    - `ExaShoppingSearch.search_web` → General price lookup.  
    - `SerperShoppingSearch.search_web` → Shopping-specific price comparisons.  

- **Error Handling**  
  - Raises an exception if initialization fails.

### **now let's see the `model` these `agents`  use**

**openai_gpt3.5_turbo model**

<img width="814" alt="d" src="https://github.com/user-attachments/assets/7b53c186-3f6b-4bb2-8a40-d7f44df6606a" />

The `LoadModel` class is responsible for loading the OpenAI GPT-3.5-turbo model when required.    

- **Model Initialization**  
  - Loads `OpenaiModels.gpt_3_5_turbo` from `taskflowai`.  
  - Ensures API keys are validated **only when called**, preventing unnecessary checks.  

- **Logging & Error Handling**  
  - Logs successful model loading.  
  - Catches and logs errors, raising an exception if loading fails.  

### **now let's talk about the `tools` these `agents` have access to** 

### exa_search or exa_shopping_search tool  (these two are mostly similar) **not much difference** *defined it seperately* 

<img width="821" alt="exa " src="https://github.com/user-attachments/assets/366d301f-b323-47ac-a6da-0c4db9ea918b" />

The `ExaSearch` class provides a web search functionality using the Exa API.  

- **Search Execution**  
  - Calls `WebTools.exa_search()` to fetch search results (imported from taskflowai).  
  - Allows specifying `num_results` (default: 5).  

- **API Key Validation**  
  - Ensures `EXA_API_KEY` is set in environment variables before execution.  

- **Error Handling**  
  - Logs failures and returns `"No data available"` if an error occurs.  

### search_articles tool

<img width="860" alt="articles" src="https://github.com/user-attachments/assets/1487e20d-8e5b-4587-bc5a-a9e49dc92cae" />

The `WikiArticles` class enables fetching Wikipedia articles related to a given query.   

- **Article Retrieval**  
  - Uses `WikipediaTools.search_articles()` to fetch relevant articles (imported from taskflowai).  

- **Logging & Validation**  
  - Logs the query and number of articles retrieved.  
  - Warns if no articles are found.  

- **Error Handling**  
  - Catches exceptions and logs errors while ensuring failures are properly raised. 

### search_images tool

<img width="851" alt="images" src="https://github.com/user-attachments/assets/697de039-e8d4-40d7-8ff3-2604b8bcb3fa" />

The `WikiImages` class is responsible for fetching relevant images from Wikipedia based on a given query.  

- **Image Search**  
  - Uses `WikipediaTools.search_images()` to retrieve images related to the query (imported from taskflowai).  

- **Logging & Validation**  
  - Logs the query and number of images found.  
  - Warns if no images are available.  

- **Error Handling**  
  - Captures exceptions and logs errors to ensure smooth execution. 

### serper_shopping_search tool
*Note: when I was building this project Serper API was down or wasn't working for me (try it)* 

<img width="821" alt="ser" src="https://github.com/user-attachments/assets/7c351e2c-2087-47db-815d-7f460de0e47b" />

The `SerperShoppingSearch` class enables price research using the Serper API but falls back on `ExaShopping` due to API downtime during project development.  

- **Web Search Execution**  
  - Uses `WebTools.serper_search()` to fetch shopping-related search results.  

- **API Key Management**  
  - Loads the API key from environment variables or a `.env` file.  
  - Raises an error if the API key is missing.  

- **Error Handling**  
  - Logs and raises exceptions if the search fails. 

### **now let's talk about the `predict` route inside `app.py` the main `endpoint`.

<img width="818" alt="pred1" src="https://github.com/user-attachments/assets/8c6b0224-ef9c-492a-aa07-d8904932bfa4" />

<img width="816" alt="pred2" src="https://github.com/user-attachments/assets/e1a39fc0-1a3d-4404-8df0-10356b3cf149" />

### **Understanding the `/predict` Endpoint**  

The `/predict` route handles image-based crop detection, processes predictions, and triggers AI-powered research for detected plants.  

### **Step 1: Receiving and Decoding Image Data**  
- The endpoint expects a **base64-encoded image** in the JSON request (`request.json["image"]`).  
- The image is **decoded** using `base64.b64decode(data)`, preparing it for processing.  
- A log entry confirms the image has been successfully received and decoded.

### **Step 2: Object Detection and Processing**  
- The decoded image is passed to `process_prediction()`, where:  
  - The image is analyzed, and detected objects are identified.  
  - The function returns `labels_text`, an error (if any), and a **processed image**.  
- If an error occurs, the API returns a **500 error response**, logging the failure.

### **Step 3: Reading Detected Objects**  
- The function `read_detected_objects(DETECTED_OBJECTS_PATH)` reads from `detected_objects.txt`, which contains unique labels (plant names) identified during detection.  
- The detected objects are logged for reference.

### **Step 4: Research and Report Generation**  
- If objects were detected, the system proceeds with **AI-driven research**:  
  - `execute_research_and_report(detected_objects)` triggers research tasks for each plant, retrieving data on:
    - **General Information** (`research_overall_web()`)
    - **Health Benefits & Risks** (`research_health()`)
    - **Growth Conditions & Farming** (`research_season()`)
    - **Market Prices** (`research_price()`)
  - Results are **structured into a dictionary** and stored in `research_results`.  
  - `generate_summarized_report(research_results)` compiles a **summary** of all findings.

- If an error occurs during research, it is logged but does not stop execution.

### **now let's see the beautiful shots how it looks when exposing `port:5000` after running `app.py`**

<img width="941" alt="lf1" src="https://github.com/user-attachments/assets/8c7ef0d0-392d-4da9-bdff-5e87f573f788" />
<img width="934" alt="lf2" src="https://github.com/user-attachments/assets/d63f6d55-2211-47d0-9048-cad8c237cddd" />
<img width="938" alt="lf3" src="https://github.com/user-attachments/assets/a1c2557e-d099-4607-8b32-9820a8c061d8" />
<img width="940" alt="lf4" src="https://github.com/user-attachments/assets/9489e011-bb8c-49a4-b282-ccdd84335329" />
<img width="944" alt="lf5" src="https://github.com/user-attachments/assets/a1b0ac3a-5579-432c-be3f-39781c90b0ef" />
<img width="938" alt="lf6" src="https://github.com/user-attachments/assets/157f3d20-68e3-4fbe-945c-0bc4585cae58" />
<img width="941" alt="lf7" src="https://github.com/user-attachments/assets/d7cded3e-d818-4779-ae0f-6a27795ac548" />
<img width="940" alt="lf8" src="https://github.com/user-attachments/assets/a8d0fc8b-380d-4b38-b238-794e6f7f2085" />
<img width="944" alt="lf9" src="https://github.com/user-attachments/assets/12c4b367-5964-4d4b-b43c-11086b3960dc" />
<img width="944" alt="lf10" src="https://github.com/user-attachments/assets/cbcbac0e-71af-4984-a0ed-e76e107c8de6" />
<img width="946" alt="lf11" src="https://github.com/user-attachments/assets/1ca25e92-e9d4-42f3-8f62-b67a5c039d50" />
<img width="944" alt="lf12" src="https://github.com/user-attachments/assets/b2d33c69-f344-49a5-b416-dce284588b7d" />
<img width="942" alt="lf13" src="https://github.com/user-attachments/assets/ece79350-58fb-4f27-89c0-c60ea2125dde" />
<img width="946" alt="lf14" src="https://github.com/user-attachments/assets/5bf34dbd-ead0-4a4c-b9b9-34acd3307093" />
<img width="946" alt="lf15" src="https://github.com/user-attachments/assets/8809abe9-c71e-441a-a998-ed61063e34e8" />
<img width="941" alt="lf16" src="https://github.com/user-attachments/assets/4d09dfe1-2761-45ad-a80f-a900e6953be5" />
<img width="941" alt="lf17" src="https://github.com/user-attachments/assets/62a6c4d0-93dc-46d4-a085-5c2dcd88ad62" />
<img width="944" alt="lf18" src="https://github.com/user-attachments/assets/c3fbda76-199b-4157-b6a7-c43aeea23977" />
<img width="935" alt="lf19" src="https://github.com/user-attachments/assets/b8b80df2-e461-4ad2-8da9-8fab663e3c20" />
<img width="936" alt="lf20" src="https://github.com/user-attachments/assets/0172f67e-ff7f-4984-bc1a-4b34a939ad17" />
<img width="933" alt="lf21" src="https://github.com/user-attachments/assets/ed9ce333-b6b4-47df-b748-1723f5317ffb" />
<img width="942" alt="lf22" src="https://github.com/user-attachments/assets/e8a7695e-3e54-4d2c-90cd-7ec1788c802a" />
<img width="942" alt="lf23" src="https://github.com/user-attachments/assets/97a019d2-beb5-493f-92f4-8d34329a18fb" />
<img width="944" alt="lf24" src="https://github.com/user-attachments/assets/cd8e2e4e-b763-486c-91eb-f27c1863832a" />
<img width="941" alt="lf25" src="https://github.com/user-attachments/assets/e1ab6031-8ed9-4149-a077-14c6c2e15678" />
<img width="958" alt="lf26" src="https://github.com/user-attachments/assets/0df3a151-7c88-479e-840d-9acc957dad8c" />

### **now let's see the send_report in `app.py` that sends the email carrying your `summarized report`

<img width="812" alt="em1" src="https://github.com/user-attachments/assets/6ff53c06-08ce-4a50-be64-9cc4adb12453" />
<img width="803" alt="em2" src="https://github.com/user-attachments/assets/a86a1ea8-6caf-4fc2-862d-10f5d4fddc9e" />

This route sends the **summarized research report** via email.  

1. **Extracts request data** – Retrieves `email` and `summarized_report`, handling key mismatches.  
2. **Formats the report** – Converts HTML into **plain text**, improving readability.  
3. **Sends the email** – Uses `send_email()`, returning **200** on success or **500** on failure.  
4. **Handles errors** – Logs exceptions and responds accordingly.

*this is `send_email()` 

<img width="815" alt="sem" src="https://github.com/user-attachments/assets/c7d81141-e1c4-483f-a9f5-1fac8e798e04" />
<img width="803" alt="sem3" src="https://github.com/user-attachments/assets/9eb5e0ad-4649-476d-9ba8-9b9ed5ed7bd8" /> 

1. **Loads credentials** – Fetches `SENDER_EMAIL` and `SENDER_PASSWORD` from environment variables.  
2. **Validates credentials** – Ensures required SMTP details exist.  
3. **Creates email** – Uses `MIMEMultipart()` to format **subject & body**.  
4. **Sends via Gmail SMTP** – Establishes a **TLS-secured connection**, logs in, and dispatches the email.  
5. **Handles failures** – Logs errors and returns `False` if unsuccessful. 

*this is how summary report looks that the `receipient receives`*

<img width="738" alt="email1" src="https://github.com/user-attachments/assets/0c05a81d-1ec0-419f-94a8-2ef84693f373" />
<img width="737" alt="email2" src="https://github.com/user-attachments/assets/0d74f7a6-21f9-4d32-8ba3-30c53c5730dc" />
<img width="729" alt="email3" src="https://github.com/user-attachments/assets/5abf160a-7334-4901-8741-01c87e1a0005" />
<img width="728" alt="email4" src="https://github.com/user-attachments/assets/25cb29c5-849b-4ce1-a28f-c86890349cf1" />

### **this is when `user` clicks `end program` in UI**

<img width="803" alt="end" src="https://github.com/user-attachments/assets/b19e3a9d-5205-4c1c-b2fb-3155a571de18" />

Handles **graceful server shutdown** when triggered from the UI.  

1. **Receives request** – Logs the shutdown initiation.  
2. **Starts a separate thread** – Calls `shutdown_server()` to prevent request blocking.  
3. **Delays execution** – Waits **1 second** before exiting.  
4. **Forces server exit** – Calls `os._exit(0)` to terminate the application.  
5. **Handles errors** – Logs any failures and returns an error response if needed. 


---
### Welcome to Deployment and CICD related things




### Guide for Developers 🌿🎇✨💚🎆🌱🎇✨💚🎆
--

### ⚠️ **Note for Developers**  

The model I am using in this project **is not the one trained with the modular code approach**. Instead, I trained it separately on **Google Colab using an NVIDIA A100 GPU**.  

Here are the training details:  
- **Dataset**: 25,000 images  
- **Epochs**: 100  
- **Compute**: A100 GPU (Colab Pro)  

If you want to train the model yourself, you are free to choose any **epoch size** based on your **compute resources (and budget 💰)**.  

### 📢 **Dataset Information**  
The dataset is **open-source** and available on **Hugging Face**:  
📌 **[100 Crops & Plants Object Detection Dataset (25K Images)](https://huggingface.co/datasets/devshaheen/100_crops_plants_object_detection_25k_image_dataset)**  

🔗 **Please give credit** if you use this dataset—it took **1.5 months** to annotate all the images!  

### ✅ **Using the Pretrained Model**  
To make things easier, I have already provided the **trained model (`best.pt`)** in the **project root directory**. You can use it directly for inference instead of retraining from scratch. Just check the **project files**, and you’ll find it ready to use! 🚀  

### 🛠 **Train the Model Yourself**  
If you want to train the model on a **larger epoch size**, I have already provided a **Colab Notebook** for training:  `notebooks/leaflogic_detection (soft).ipynb ` 

Simply open the notebook in **Google Colab**, adjust the training parameters as needed, and run the training process! 🔥  
--



## License 📜  

This project is licensed under the **MIT License**.  
Feel free to use, modify, and share it with proper attribution. For more details, see the [LICENSE](LICENSE) file. 🌟  ....

