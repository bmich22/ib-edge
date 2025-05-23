# ib-edge
IB EDGE is an ecommerce website that offers tutoring services for IB (International Baccalaureate) Diploma Students. Visitors can create a profile in order to buy tutoring packages, book sessions and track their progress.The application implements role-based authentication with a personalized dashboard and secure Stripe payments. IB EDGE has two tutors, a brother-sister team currently studying at universities in the Netherlands.  They are expert tutors in English SL & HL, Extended Essay and TOK (Theory of Knowledge), Math SL & HL and Physics SL & HL. IB EDGE offers three packages, Bronze, Silver and Gold. They range in size from four tutoring sessions to twelve with additional benefits like free downloads and email/chat support.

This project was created to meet the needs of high school students seeking specialized IB tutoring by providing a structured, session-based platform. It offers paid access to tutoring packages, personalized dashboards for both students and tutors, and admin-level tools for tracking purchases and sessions. The system also features secure, role-based access control to ensure appropriate permissions across user types. The target audience includes IB students in need of academic support and parents that may be looking for tutors for their choldren.

The live version of the recipe hub project is [here](https://ib-edge-5d506d674ecb.herokuapp.com/).


### Screenshots of Home Page
| Large and Medium Screen | Small Screen |
| ----------- | ----------- |
| ![large and med screen](/media/readme-images/home-large-screen.png)| ![small-screen](/media/readme-images/home-small.png) |

### UX / Wireframes / User Stories / Database Models
The initial building blocks of the project were the wireframes and user stories. The wireframes served as a visual blueprint for the layout and structure of the site and the user stories provided insight into what functions were needed. Planning the databases helped visualize how the data is linked and how the databases could be queried to pull the desired information.

WIREFRAMES

| Home | About | Packages | User View | Student Profile
| ---- | ----- | ----- | ---- | ------------- 
| ![home](/media/readme-images/wf-homepage.png) | ![about](/media/readme-images/wf-about.png) | ![packages](/media/readme-images/wf-packages.png) | ![user-view](/media/readme-images/wf-user-view.png) | ![student-profile](/media/readme-images/wf-student-profile.png)

USER STORIES

![user-stories](/media/readme-images/user-stories.png) |

MODELS

![models](/media/readme-images/models.png) 

### Features
| Feature | Screenshot 
| ------- | ----------
| **Responsive Design** The site is responsive and displays nicely on all screen sizes.  Bootstrap was used to format the content, utilizing its columns and grids, its container-fluid and image-fluid, as well as utility styling on text, padding and margins. The user can easily use their mobile device to view / add / edit content.|  ![mobile-utility](/media/readme-images/mobile-utility-3.png) 
| **About Page** The about introduces our tutors and provides a bio of each of them. |  ![image](/media/readme-images/about-large-screen.png) 
| **Packages Page** The packages page displays the three packages on offer, bronze, silver and gold level.  Users can purchase a package via the button at the bottom of each package.  If site visitors try to buy they will be routed to sign up first. |  ![image](/media/readme-images/packages-large-screen.png) 
| **Contact Page** The contact page displays a simple contact form that visitors can fill in name, email and message and send to the site admin. Messages are stored in a database.  Any site visitor can send a message via the contact form.  The contact form has a honey pot field for spam protection |  ![mobile-utility](/media/readme-images/packages-large-screen.png) 
| **Authentication and Authorization** The site utilizes django-allauth for secure registration, login, and logout. A custom UserProfile model includes role flags (e.g., is_tutor, is_superuser) to manage access. Views are protected based on user roles, with session-based state reflected in the navbar and dashboard, and URL access is restricted using @login_required and role-specific checks. 
| **Student Dashboard** The student dashboard has three columns.  Column one shows the number of sessions they have available, this number is calculated by the number of sessions purchased minus sessions logged by a tutor.  If the student has sessions available, the 'book session' button will display and the student will be able to go to the tutor's calendar to book a session (this is an upcoming feature). Column two lists the tutoring sessions that have been completed, this is triggered by the tutor filling in the 'log session' form. Column three shows a list of packages purchased, the date, subject and expiration date. | ![image](/media/readme-images/student-dashboard.png)
| **Tutor Dashboard** The tutor dashboard has links to utility features, most importantly the log session form. Future features are a functioning link to their calendly to check their calendar, a link to view current students. |![tutor-dashboard](/media/readme-images/tutor-dashboard.png)
| **Admin Dashboard** The admin dashboard has links to utility features, most importantly, the link to the admin panel so  the site administrator doesn't have to sign in to the admin panel separately. Site admins can also log a tutoring session, they can check contact message via the link that will take them direct to the contact messages in the admin panel. There is also a link to add/edit/delete the Packages and they can also add a tutor |![admin-dashboard](/media/readme-images/admin-dashboard.png)
| **CRUD** 
| **User Profile Form** After sign up the user is taken to the user profile where they are asked to fill in their first and last names, their grade level and a parent's email.  This form can be editied by clicking on the EDIT PROFILE button next to the welcome message.  | ![image](/media/readme-images/edit-user-profile.png)
**Admin Add/Edit/Delete Package Form** When the site administrator is signed in, they can add, edit or delete any package directly on the packages page.  | ![image](/media/readme-images/admin-edit-packages.png)
**Tutor Log Session Form** The tutor can access the log session form via their dashboard. In the form the tutor can choose the student name from the drop-down list, click on the calendar for the date of the session, choose a time from the drop-down list, enter notes about the session (not mandatory) and then click the log session button. The tutor will see a confirmation message in their window that the session has been logged. This is entered into the session database and triggers a calculation of the total sessions remaining for this student.  In the student's user profile this will be updated showing the number sessions remaining, and a list of the sessions logged and by which tutor.   | ![image](/media/readme-images/tutor-log-session.png) ![image](/media/readme-images/update-total-sessions.png)
| **eCommerce** The application incorporates e-commerce features using Stripe Checkout for secure package payments. A  session counter reflects purchased sessions in real time, while Stripe webhooks ensure user accounts are updated accurately after each transaction. Upon successful payment, the user-profile page displays a confirmation message and the customer email (entered before purchase) receives an email confirmation. There is error handling built in to ensure that if a student hits the back button or leaves the page, the session goes back to parent email page and starts again.  Here the student must also choose a subject from the drop-down list.  These two entries must be filled in before going forward to the Stripe checkout page.| ![image](/media/readme-images/purchase-process.png)

### Marketing and SEO
| Tool | Screenshot
| ---- | ----
| Email Marketing with Mailchimp Embedded Sign-Up Form | ![image](/media/readme-images/mailchimp-signup-and-verify.png)
| Facebook Business Page (mockup) | ![image](/media/readme-images/facebook-page.jpg)
| Keywords | ![image](/media/readme-images/keywords-terms-seo.png)

### Not Working
The booking system is not connected to any real Calendy accounts.  

### Future Features
**Integrated Booking and Video Call System**
Currently the students will book via the tutor's Calendly. An upgrade would be a system that is integrated where the student can also sign in and onto the sessions, all via the IN EDGE site.

**Give Tutors access to sessions adamin panel**
Tutors should have access to the sessions admin panel so they can see notes from former sessions.

**Calculate Hours Worked**
Tutors should be able to invoice based on the complete sessions.

**Free Download and Links**
Add a tab to the navbar so students can find study tips and subject-focused notes to download.  This area would also have links to other IB related sites.

### Tools and Technologies Used
| Tool | Technology
| ---- | ----------
| [ChatGPT] | https://chatgpt.com/ | AI chatbot developed by OpenAI. to help with perfecting code and for general how-to instructions.
| [GitHub](http://github.com//) | Version control platform used for storing and managing this project.
| [VS Code](https://code.visualstudio.com///) | Local code editor with Git integration.
| [Django==4.2.18](https://www.djangoproject.com/) | Python web app framework.|
| [Django AllAuth](https://docs.allauth.org/en/latest/) | django-allauth is package that handles authentication features such as user registration, login/logout, email verification, password reset, and social login.|
| [Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest//) | a Django package that makes it easy to style and format form layouts using Bootstrap or other CSS frameworks, without writing custom HTML for each form field.|
| HTML 5| The standard markup language for creating web pages and structuring content.
| CSS| A styling language used to design and layout web pages, enhancing their appearance and responsiveness.
| [Bootstrap 5.3.3](https://getbootstrap.com/docs/5.3/getting-started/introduction/) | A front-end framework that simplifies web development with pre-styled components and a responsive grid system. Used to format the content, utilizing its columns and grids, its container-fluid and image-fluid, as well as utility styling on text, padding and margins.
| [Google Fonts](https://fonts.google.com/) | A collection of free, web-optimized fonts.
| JavaScript | Scripting language for web pages, used here for the edit comments functionality.
| [Python](https://www.python.org/)| Programming language to create web applications, used here inside the django framework.
| [Whitenoise](https://whitenoise.readthedocs.io/en/latest//) | A Python package that allows your Django app to serve  files (like CSS, JS, and images) directly in production.
| [PostgreSQL](https://www.postgresql.org/) | An open-source relational database system used for storing and managing data. Used for managing the recipe, member and comment databases and the built-in User database.
| [Google Chrome Dev Tools](https://developer.chrome.com/docs/devtools) | Web development tools built into Chrome for debugging and optimizing web applications
| [Heroku](http://heroku.com) | A cloud platform that simplifies the deployment and hosting of web applications, used to deploy the-recipe-hub.
| [Stripe](https://stripe.com/) | A payment processing platform that allows businesses to securely accept online payments, including credit cards, digital wallets (like Apple Pay), and bank transfers.
| [Balsamiq](https://balsamiq.com/) | A wireframing tool utilized in the planning phase of IB EDGE and also to mock up the Facebook Business Page.
| [Flake8](https://flake8.pycqa.org/en/latest/) | A Python linting tool that checks for style guide enforcement and potential errors in code. Used inside VS Code.
| [Black 2024.6.0](https://black.readthedocs.io/en/stable/) | A Python code formatter that ensures consistent code style by automatically formatting code according to best practices. Used inside VS Code.
|[Gunicorn==20.1.0](https://gunicorn.org/) | A Python WSGI HTTP server used to serve web applications built with Django and acts as intermediary with Heroku.

### Automated Testing Manual

![image](/media/readme-images/testing-user-profile-model.png) |
![image](/media/readme-images/testing-checkout-app.png) |
![image](/media/readme-images/testing-sessions-app.png) |

### Manual Testing 
Continuous manual testing was performed as features were added to the project to ensure forms were loading and data was processed to and from the database. Responsiveness was tested inside Google Chrome Dev Tools to ensure the site is visually pleasing on all screen sizes. In addition, the HTML, CSS, and Python were run through linters to ensure clean, consistent, error-free code. The outcomes are below.
| Checking | Screenshot
| ---- | ----------
**Sign Up Process and Profile Update**  | ![image](/media/readme-images/manual-test-1.jpg) |
**Error handling - Forms** When the site administrator is signed in, they can add, edit or delete any package directly on the packages page.  | ![image](/media/readme-images/manual-test-error-handling-forms.jpg) |
**Error handling - Forms** When the site administrator is signed in, they can add, edit or delete any package directly on the packages page.  | ![image](/media/readme-images/manual-test-error-handling-forms-2.jpg) |
**Checking Admin Panel/User Profile for update of Total Sessions Num and Subject is recorded** When the site administrator is signed in, they can add, edit or delete any package directly on the packages page.  | ![image](/media/readme-images/admin-panel-subjects-sessions.png) |

| Linter | Outcome |
| ---- | --------- | 
|[Code Institute Python Linter](https://pep8ci.herokuapp.com/) | All .py files were run through the CI Python Linter. |
|[W3C HTML Validator](https://validator.w3.org/) | All .html documents were run through the validator. | 
[W3C HTML Validator](https://jigsaw.w3.org/css-validator/) | No errors on base.css. |

| File        | [HTML Validator](https://validator.w3.org/) | [PEP8](https://pep8ci.herokuapp.com/) |
| ----------- | ------------------------------------------- | ------------------------------------- |
| `base.css`  | no errors                                   |                                       |
| `base.html` | flags Django template tags, otherwise clear |                                       |
| CHECKOUT APP             | HTML                                        | PEP8                                                         |
| ------------------------ | ------------------------------------------- | ------------------------------------------------------------ |
| `checkout_cancel.html`   | flags Django template tags, otherwise clear |                                                              |
| `checkout_success.html`  |                                             |                                                              |
| `checkout.html`          |                                             |                                                              |
| `confirmation_body.html` |                                             |                                                              |
| `who_is_paying.html`     |                                             |                                                              |
| `checkout/admin.py`      |                                             | no errors                                                    |
| `checkout/apps.py`       |                                             | no errors                                                    |
| `checkout/forms.py`      |                                             | no errors                                                    |
| `test_views.py`          |                                             | too long line error, line 30, every fix caused another error |
| `test_models.py`         |                                             | no errors                                                    |
| `urls.py`                |                                             | no errors                                                    |
| `models.py`              |                                             | no errors                                                    |
| `views.py`               |                                             | no errors                                                    |
| `webhook_handler.py`     |                                             | no errors                                                    |
| `webhooks.py`            |                                             | no errors                                                    |
| CONTACT APP              | HTML | PEP8      |
| ---------------------- | ---- | --------- |
| `contact_success.html` |      | no errors |
| `contact.html`         |      | no errors |
| `admin.py`             |      | no errors |
| `apps.py`              |      | no errors |
| `forms.py`             |      | no errors |
| `models.py`            |      | no errors |
| `urls.py`              |      | no errors |
| `views.py`             |      | no errors |
| HOME APP     | HTML                                        | PEP8      |
| ------------ | ------------------------------------------- | --------- |
| `about.html` | flags Django template tags, otherwise clear |           |
| `index.html` | flags Django template tags, otherwise clear |           |
| `apps.py`    |                                             | no errors |
| `views.py`   |                                             | no errors |
| IB_EDGE      | HTML | PEP8      |
| --------- | ---- | --------- |
| `urls.py` |      | no errors |
| PACKAGES APP                          | HTML                                                                                    | PEP8      |
| ----------------------------- | --------------------------------------------------------------------------------------- | --------- |
| `package_confirm_delete.html` | flags Django template tags, otherwise clear                                             |           |
| `package_form.html`           | flags Django template tags, otherwise clear                                             |           |
| `packages.html`               | calls trailing slash on void elements, it is `<hr>` but Prettier keeps changing it back |           |
| `admin.py`                    |                                                                                         | no errors |
| `apps.py`                     |                                                                                         | no errors |
| `forms.py`                    |                                                                                         | no errors |
| `models.py`                   |                                                                                         | no errors |
| `urls.y`                      |                                                                                         | no errors |
| `views.py`                    |                                                                                         | no errors |
| SESSIONS APP       | HTML                                        | PEP8      |
| ------------------ | ------------------------------------------- | --------- |
| `log_session.html` | flags Django template tags, otherwise clear |           |
| `test_models.py`   |                                             | no errors |
| `test_views.py`    |                                             | no errors |
| `admin.py`         |                                             | no errors |
| `forms.py`         |                                             | no errors |
| `models.py`        |                                             | no errors |
| `views.py`         |                                             | no errors |
| USER_PROFILES APP      | HTML                                                                                    | PEP8      |
| ---------------------- | --------------------------------------------------------------------------------------- | --------- |
| `admin_dashboard.html` | flags Django template tags, otherwise clear                                             |           |
| `tutor_dashboard.html` | flags Django template tags, otherwise clear                                             |           |
| `user_profile.html`    | calls trailing slash on void elements, it is `<hr>` but Prettier keeps changing it back |           |
| `admin.py`             |                                                                                         | no errors |
| `apps.py`              |                                                                                         | no errors |
| `forms.py`             |                                                                                         | no errors |
| `models.py`            |                                                                                         | no errors |
| `signals.py`           |                                                                                         | no errors |
| `urls.py`              |                                                                                         | no errors |
| `views.py`             |                                                                                         | no errors |
| `test-forms.py`        |                                                                                         | no errors |
| `test_models.py`       |                                                                                         | no errors |
| `test_views.py`        |                                                                                         | no errors |
| `test_signals.py`      |                                                                                         | no errors |


### Deployment

Heroku was used to deploy the site.
1. Sign up for Heroku account.
2. Create a new App and name it a unique name.
3. Complete Settings section, add Config Vars:
    * database - PostgreSQL
    * disable collect
4. Go to Deploy section, select Github and confirm, choose the ib-edge repository, click connect to link Heroku to the Github repository code.
5. Click deploy, manual deploy
6. Wait for the message, "Your app was successfully deployed" then click VIEW.

### Acknowledgements
Thank you to [Spencer Barriball](https://github.com/5pence?tab=repositories), my mentor at Code Institute.





