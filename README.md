[![DOI](https://zenodo.org/badge/685568968.svg)](https://zenodo.org/doi/10.5281/zenodo.11508669)

# Interactive Management App

The Interactive Management App project will design and build an open source tool for conducting Interpretive Structural Modeling (ISM) research with participants



## Table of Contents
- [Background](https://github.com/VERSO-UVM/Interactive-Management-App/blob/main/README.md#Background)
- [Install](https://github.com/VERSO-UVM/Interactive-Management-App/blob/main/README.md#Install)
- [Research](https://github.com/VERSO-UVM/Interactive-Management-App/blob/main/README.md#Research)
- [Requirements](https://github.com/VERSO-UVM/Interactive-Management-App/blob/main/README.md#Background)
- [Core Action](https://github.com/VERSO-UVM/Interactive-Management-App/blob/main/README.md#Requirements)


## Background

The objective of this project is to design and build an open source browser-based tool for conducting Interpretive Structural Modeling (ISM) research with participants. It includes a series of questions about pairs of variables (called "factors") and whether or not those factors are related to one another. The software will produce a flow diagram of the relationships between factors as identified by the participant, and provide the researchers with one flow diagram that averages the data across all participants in a particular study. The flow diagram will suggest factors that are likely more effective to address first, and factors that are likely to follow or become easier to address as a result of addressing earlier factors.

ISM is one of a number of core methodologies that groups and teams can benefit from when working to address complex problems. The hope is that a web-based version can increase accessibility for communities and organizations to use ISM in fostering collective intelligence for informing social transformation.

Interpretive Structural Modeling (ISM) is a method for representing and analyzing complex systems. It was developed by J. Warfield in 1973 and has been used in a variety of fields, including business, engineering, education, and healthcare.

The method builds a flowchart of the relationships between variables that influence a desired outcome for a system, like “a sustainable environment” or “an inclusive workplace.” It does this by creating a network that represents the relationships between the variables that affect a system. The nodes in the network represent factors, and the arrows (called “directed ties” or “directed edges” in network terminology) represent the relationships between the factors. The direction of the edge indicates the direction of the influence.

ISM uses a four-step process to develop a model of a system:

- Identify the factors that affect the system. This step uses a survey of participants to gather a list of factors that affect a specified outcome for the system.
- Ranking the factors. In this step, a researcher groups factors from the surveys that are similar. Then, they pick the most important factors mentioned by the participants for the participants to keep working with.
- Determine the relationships between the factors. This step involves asking one participant or a group of participants the question "Does factor A influence factor B?" for each possible relationship and recording the answer as a directed edge in the network.
- Construct the flowchart. This step uses a network node ordering algorithm to identify factors (the nodes) that come before each other in solving the problem. It then displays the ordered network as a flowchart with factors that come first farthest to the left.

Here are some of the benefits of using ISM:

- It is a visual method that is easy to understand and communicate.
- It can be used to model complex systems.
- It can be used to identify the key elements of a system and the relationships between them.
- It can be used to identify potential problems in the system and to develop strategies for improving the system.

Here are some of the limitations of ISM:

- It is a subjective method that depends on the judgment of the people involved in the modeling process.
- It can be time-consuming and labor-intensive to develop an ISM model.
- It can be difficult to validate the results of an ISM model.

## Install

### Running locally

These instructions are designed for MacOS & GNU/Linux users.  
**Windows users:** [Using WSL](https://learn.microsoft.com/en-us/windows/wsl/install) (Windows Subsystem for Linux) is recommended.

### Requirements

Install the following tools using their instructions:

- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)- Python version manager
- [nvm](https://github.com/nvm-sh/nvm) - Node version manager

#### Running locally

**Setup pyenv & nvm**

```sh
# Python
pyenv install # If the version already exists, no need to re-install
# Node.js
nvm install
```

**Install dependencies**

```sh
# Python
pip install -r requirements.txt
# Node.js
corepack install # Sets up npm
npm install
```

**Run the app**

```sh
python wsgi.py --port=5001 --host=localhost --debug
```

Then visit http://localhost:5001

### Python Everywhere

## Research

### Relevent Research
Razzante, R. J., Hogan, M., Broome, B., Tracy, S. J., Chawla, D., & Skurzak, D. M. (2023). Interactive Management Research in Organizational Communication. Management Communication Quarterly, 0(0). [https://doi.org/10.1177/08933189231159386](https://doi.org/10.1177/08933189231159386)

### Existing Projects

- [https://github.com/jjs0sbw/bsmp](https://github.com/jjs0sbw/bsmp)
- [https://github.com/varchasvshri/ISM_Analysis](https://github.com/varchasvshri/ISM_Analysis)
- [https://github.com/cran/ISM](https://github.com/cran/ISM)
- [https://github.com/Dr-Eti/ISMiR-ISM_in_R](https://github.com/Dr-Eti/ISMiR-ISM_in_R)



## Requirements

1. Tool must perform Steps 2-4 of the ISM process: (2) manual ranking by the researcher, (3) determining factor relationship, and (4) constructing the flowchart
2. Ability to add factors
3. Web user interface (supported on Chrome, Firefox, Edge)
4. Use math from Warfield, or equivalent modern network ordering visualization algorithm
5. Results can be saved to a local computer



## Core Actions

### I want to load factors I have selected for exploration

Factors are the text descriptions of things that we think are important. These factors are likely structured as a csv, but can include manual entry of factors individually. The csv may be already in order, or it may not. Some files may also have a column with a numberic value that may be used to order them, in some cases it may be as simple as 1, 2, 3 or it may be a count value like 300 votes. This means some times if there is numeric information it may need to be in ascending or descending order.
MVP: Upload a CSV and order it by a column that lists order of importance with 1 being the most important

### If unranked, I want to manually rank them

If there is no ranking there needs to be a way to manually order them. This could be drag and drop, or listing the items with a space to add a value.
MVP: This is a stretch goal for MVP

### I want to select a subset of factors for structuring

There are often a lot of factors in the upload and we want to select a subset. There are a couple of approaches, like manually selecting what you want to keep, or just keeping a selected number of the top factors.
MVP: Select the top # of results with a field to enter the number of top factors that should be kept

### I want to record relationships and rationales for pairs of factors

Now there are a list of factors we need to determing the relationship between all the factors. This can be binary (like the original .exe) or it can be a scale like 1-5 or 1-10. We want to select the type of relationship, and then work through each pairing, entering the relationship value manually which is then stored in a new dataset of these relationships. The order of the relationships may need to be randomized, or may need a methodology that allows some but not all to be done. It may also be useful to think about an export and import feature here so if the session is interrupted you can save and reload where you were.
MVP: Display two factors and a field where a value from 1-5 can be entered (being able to select binary is a stretch goal) and a button to submit it for processing (automatically?)

### I want the ordering of factors to be calculated

After entering all these relationships we then need to have the overall relationship calculated by a model (this will be provided by the sponsor) which will give the overall relationship weights. This will be a new dataset and will be automatically done once the previous step is complete. The ability to select which model you use will be helpful.
MVP: automatically process with the default model

### I want to see a visual depiction of the ordered factors

Displaying the flow diagram for the participants is useful in order to provide the result to the team. The flow diagram will have an order of impact from left going to right (althought worthwhile to consider vertical layouts too) with a graph style of edges and nodes displaying with the weight of the relationships.
MVP: display a simple png with the factors and lines showing the relationship ordered from left to right

### I want to export the results

After this is all done, we want to export all the datasets that have been created for analysis. This can be as simple as a set of CSVs with appropriate names. Ideally it would also include the PNG.
MVP: Save all datasets as CSVs




## Feature Requests

1. Record a reason for each factor relationship selection (the reason why you think A impacts B). (From Mike Hogan: “As part of a stigmergic approach to collective intelligence design, it is valuable to record these arguments, as it allows subsequent reflection, revision of arguments and system models”)
2. Tracks Workshop Info - Includes text fields for Trigger Questions, Context Statement, Title, Date, Host Organization, Location and Objectives Workshop Info
3. Can Add Participants - Adding and editing Participants includes fields for First and Last name, Job Title, Address, State, City, Zip, Country, Type (drop down: Participant, Observer and Facilitator), Telephone and buttons to add new and save. Additionally you can search current participants, remove search and filter by type. At the bottom right is a delete button for participants Participants
4. Add and Edit Ideas - Ideas include open test field for Idea and Clarification and a small text field for Label. Category is a dropdown populated from elsewhere Add/Edit Ideas
5. Voting - Voting displays participants, Ideas with vote counts and Structuring Sets area with filtering dropdown and an add, edit and delete button Voting
6. Structuring - Structuring has a variety of UX elements for building relational structures between ideas. There is a Select Structured Set dropdown, Keyword and Context Statement text field, left and right text field and a drop down for orientation. On the lower half there are toggles for fullscreen, clarifications, exporting the graph, viewing the graph and settings along with a Yes and No button Structuring
7. Tools - In the top bar menu there is a Tools section that allows one to import or export both ideas and participant lists (unsure of specs for those files) Tools
8. Linked ISM with Rationale (a desktop argument mapping software).

- As such, if you recorded the dialogue during an ISM structuring session, you could then go and document the argument structure that lead a group to a ‘yes’ or ‘no’ decision (i.e., in response to the question, Does X influence Y?) You’ll see the basic design in Figure 6 in the final attachment
- Obviously, if we use a swarm approach to collective intelligence (i.e., which could involve a more independent and partially asynchronous deliberation and voting strategy), then the deliberation process would be different, it would be recorded differently, and it would not be facilitated in the same way we do when working face-to-face with a group.
- However, the feature could be adapted and used to record large group deliberation linked to structures generated using ISM.

9. Remote participant functionality
10. Save to the cloud/a remote server
11. Shareable as survey to users
12. Results of multiple ISM sessions can be aggregated
13. Permissions for Admin and Survey Participant
14. Likert scale relationship specification functionality

- Replace the ‘yes’ and ‘no’ relationship method with a rating (i.e., weighting of the strength of relationships on a scale of 1 to 5).
- This could be useful for groups as they reflect on the paths of influence or action in models, and it would be particularly useful in action structures (e.g., Does Action A support Action B?) as groups work to identify pathways of action to leverage for collective design/implementation that emerge from ISM modelling work.
- understood how underlying the matrix structure and the systems models groups are generating is an argument structure

15. Every path and link in the model derives from an argument that emerges at the group level during facilitation
