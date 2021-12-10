# Overview
This document contains all current functional and non-functional requirements we have for our project. These requirements show what goals we must meet for our project, and how they are achieved. 
## Functional Requirements
### Login/Create Account Function
- FR1. Users shall have to login to access the application.
- FR2. User’s information shall be stored in a database.
- FR3. The create account function shall require a password and email address.
- FR4. The login function shall have a button that clears all text fields.
- FR5. The create an account function shall allow you to create a bio.
### Home Screen
- FR6. Users shall have the home page displayed after a successful login.
- FR7. Users shall be able to access and change app settings from an icon on the home screen.
- FR8. Users shall be able to access and change profile settings from an icon on the home screen.
- FR9. The home screen shall allow the user to view individual workout plans for each day of the week.
- FR10. The favorites screen and explore screen shall be accessible from the home page.
### Search Function
- FR11. Users shall have the ability to search for workouts by combining tags or the name of the workout.
- FR12. Tags shall consist of the associated muscles that it is directed towards and the “type” of exercise that it is (eg. push, pull).
- FR13. The search function shall return relevant results and omit unrelated workouts.
- FR14. The search function shall return no results if the input term has no matches.
- FR15. The search function shall be accessible from a button on the home page.
### Add Workout Function
- FR16. Users shall be able to choose from a library of workouts to create their own workouts.
- FR17. Users shall be able to use the search function to help them find workouts.
- FR18. The added workout shall be displayed on the day selected on the home page.
- FR19. Users shall be able to save created workouts using the favorite function.
- FR20. Users shall be able to upload workouts to the explore page.
- FR21. The workouts shall be saved to the users account so that it will still be there every time they log in.
## Non-Functional Requirements
### Home Screen
- NFR1. The home screen shall only appear if the user has successfully logged in or created an account.
- NFR2. The profile screen shall give users the ability to reset their password using Firebase’s password reset functionality.
- NFR3. There shall be two buttons that change the theme of the app using Kivy’s built in theme manager.
- NFR4. The profile screen shall give users the ability to edit their bio through a text field.
- NFR5. The heart icon shall pull favorite workouts from the user database favorites collection.
### Login/Create Account Function
- NFR6. The login function shall require a correct combination of email and password via firebase to authenticate users.
- NFR7. The login screen and create account screen shall be the only screens accessible by users until a successful login has been validated by firebase.  
- NFR8. The create account function shall require the bio to be less than or equal to 350 characters.
- NFR9. The create account function shall require a password with a minimum of 6 characters.
- NFR10. The create account function shall require an email address with valid email parameters (@___.com is a valid email).
### Search Function
- NFR11. Workouts shall be placed with related tags or keywords in the firebase database to allow users to search by tag.
- NFR12. Search results shall be displayed in less than 2 seconds.
- NFR13. The search function shall display no results and no errors if the firebase database is unable to match the user input term to a keyword.
- NFR14. The search function shall be able to display all of the search results without visual issues regardless of display size.
- NFR15. Tags shall always start with a hashtag and require a space before another one is added.
### Add Workout Function
- NFR16. The user database shall be updated whenever a user adds a workout.
- NFR17. The search function shall be called when the user clicks the add button on the home page.
- NFR18. Users shall be able to upload their workouts to the firebase database in less than two seconds.
- NFR19. The reps and sets popup shall display in less than a second after choosing an exercise to add.
- NFR20. The exercise shall not be added to the workout if the reps or sets text fields are empty.
## Software Aritfacts
Below are the links to all of our previously created artifacts that contributed to the development of our project.
1. [Presentation](http://https://github.com/AboveLogic/GVSU-CIS350-TheTIA/blob/master/docs/TIA%20Presentation%202.pdf "Presentation")
2. [Use Case Diagrams](http://https://github.com/AboveLogic/GVSU-CIS350-TheTIA/tree/master/artifacts/use_case_diagrams "Use Case Diagrams")
3. [Proposal](http://https://github.com/AboveLogic/GVSU-CIS350-TheTIA/blob/master/docs/proposal-template.md "Proposal")
4. [Gantt Chart](http://https://github.com/AboveLogic/GVSU-CIS350-TheTIA/blob/master/docs/gantt_chart.drawio.png "Gantt Chart")
5. [Original SRS](http://https://github.com/AboveLogic/GVSU-CIS350-TheTIA/blob/master/docs/software_requirements_specifications.md "Original SRS")
6. [High Level Tasks](http://https://github.com/AboveLogic/GVSU-CIS350-TheTIA/blob/master/docs/high-level-tasks.md "High Level Tasks")
