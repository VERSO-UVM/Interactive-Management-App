# Interactive Management App
ORCA Project 2023-2024

The objective of this project is to design and build an open source browser-based tool for conducting Interpretive Structural Modeling research with participants. It includes a series of questions about pairs of variables (called "factors") and whether or not those factors are related to one another. The software will produce a flow diagram of the relationships between factors as identified by the participant, and provide the researchers with one flow diagram that averages the data across all participants in a particular study. The flow diagram will suggest factors that are likely more effective to address first, and factors that are likely to follow or become easier to address as a result of addressing earlier factors.

## Research 
Razzante, R. J., Hogan, M., Broome, B., Tracy, S. J., Chawla, D., & Skurzak, D. M. (2023). Interactive Management Research in Organizational Communication. Management Communication Quarterly, 0(0). [https://doi.org/10.1177/08933189231159386](https://doi.org/10.1177/08933189231159386)

## Reference App
We only have the EXE file, it will only work on windows and requires Java Runtime 1.6 but will run on more modern version of Java ([Download Java](https://www.java.com/download/ie_manual.jsp))

### Screenshots of the Reference App

#### Workshop Info
Includes text fields for Trigger Questions, Cotnext Statement, Title, Date, Host Organization, Location and Objectives
![Workshop Info](https://github.com/VERSO-UVM/interactive-management-app/blob/main/references/workshop_info.png)

#### Participants
Adding and editing Participants includes fields for First and Last name, Job Title, Address, State, City, Zip, Country, Type (drop down: Participant, Observer and Facilitator), Telephone and buttons to add new and save. Additonall you can search current participants, remove search and filter by type. At the bottom right is a delete button for participants
![Participants](https://github.com/VERSO-UVM/interactive-management-app/blob/main/references/participants.png)

#### Add and Edit Ideas
Ideas includes open test field for Idea and Clarification and a small text field for Label. Category is a dropdown populated from elsewhere
![Add/Edit Ideas](https://github.com/VERSO-UVM/interactive-management-app/blob/main/references/add_edit_idea.png)

#### Voting
Voting displays participans, Ideas with vote counts and Structuring Sets area with filtering dropdown and an add, edit and delete button
![Voting](https://github.com/VERSO-UVM/interactive-management-app/blob/main/references/voting.png)

#### Structuring
Structring has variety of UX elements for building relational structures between ideas. There is a Select Structured Set dropdown, Keyword and Context Statement text field, left and right text field and a drop down for orientation. On the lower half there are toggles for fullscreen, clarificaitons, exporting the graph, viewing the grapph and settings along with a Yes and No button
![Structuring](https://github.com/VERSO-UVM/interactive-management-app/blob/main/references/structuring.png)

#### Tools
In the top bar menu there is a Tools section that allows one to import or export both ideas and participant lists (unsure of specs for those files)
![Tools](https://github.com/VERSO-UVM/interactive-management-app/blob/main/references/tools.png)

#### Saving
Files can be saved as *.ism, ISM files are InstallShield Project files (which are structurely very similar to . msi files)

## other projects out there
* [https://github.com/jjs0sbw/bsmp](https://github.com/jjs0sbw/bsmp)
* [https://github.com/varchasvshri/ISM_Analysis](https://github.com/varchasvshri/ISM_Analysis)
* [https://github.com/cran/ISM](https://github.com/cran/ISM)
* [https://github.com/Dr-Eti/ISMiR-ISM_in_R](https://github.com/Dr-Eti/ISMiR-ISM_in_R)
