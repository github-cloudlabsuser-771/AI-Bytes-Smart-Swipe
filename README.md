# AI-Bytes-Smart-Swipe
### **SmartSwipe.ai** is a Generative AI App which informs users about the best credit card to use for each purchase, optimizing spending and enhancing the user experience.

**Capgemini Microsoft A4 Enablement Innovate Hackathon** Use Case Details:
**F-1** How might we integrate real-time credit card reward optimization into the existing contactless payment process to enhance user experience?

In the financial industry, numerous credit cards offer various plans and rewards. Navigating these options can be cumbersome and time-consuming for customers, making it challenging to maximize benefits. Generative AI presents a solution to simplify this process, seamlessly integrating with existing contactless payment methods. This tool can inform users about the best card to use for each purchase, optimizing spending and enhancing the user experience. By analyzing the rewards of each credit card in real-time, it suggests the most advantageous option, whether it's earning travel points or cashback. This would not only enhance the shopping experience but also contribute to better financial management, ensuring that consumers are making the most of their spending in alignment with their financial strategies and goals.

**Parameters:**
- Prioritize user privacy and ensure compliance with financial regulations and data protection laws.
- Ensure compatibility with a wide range of credit cards and banks to maximize applicability.
- Incorporate elements that enhance user engagement and trust in the application's recommendations.
- Consider how the application can contribute to users' overall financial well-being beyond immediate rewards.
- Explore potential integrations with emerging technologies like smart wearables or AR/VR interfaces.
- Implement a feedback mechanism for users to provide input on recommendations and app functionality, facilitating continuous improvement.

# How to build and run the SmartSwipe.ai Django Web App ?

### GitHub and Local Environment
1. Clone the repo from GitHub
`git clone https://github.com/github-cloudlabsuser-771/AI-Bytes-Smart-Swipe.git`
2. Setup your Azure API Secrets in OS environment variables
`OPENAI_API_KEY` and `SEARCH_KEY`

### Development Environment (`PyCharm` OR `VS Code`)
1. Go to the repo directory path and setup `venv`
`python -m venv venv`
2. Activate the `venv` on terminal
`source venv/bin/activate`
3. Install all required dependencies for project
`pip install -r requirements.txt`
4. Do the migration to update Django database schema
`python manage.py makemigrations`
5. Confirm the migration
`python manage.py migrate`
6. Create superuser for Admin access
`python manage.py createsuperuser`
7. Run the project on localhost
`python manage.py runserver`                            // This will run on http://127.0.0.1:8000/


### Screens:
1. Login
<img width="1440" alt="Screenshot 2024-05-04 at 6 03 52 PM" src="https://github.com/github-cloudlabsuser-771/AI-Bytes-Smart-Swipe/assets/167456961/adf53696-f44b-40ce-a8b6-dec78b656a1e">

2. Register
<img width="1440" alt="Screenshot 2024-05-04 at 6 04 03 PM" src="https://github.com/github-cloudlabsuser-771/AI-Bytes-Smart-Swipe/assets/167456961/1731c43c-6b76-4e3d-a7c9-d033a8cf494c">

3. Chat Dashboard
<img width="1440" alt="Screenshot 2024-05-04 at 6 04 15 PM" src="https://github.com/github-cloudlabsuser-771/AI-Bytes-Smart-Swipe/assets/167456961/08e39856-39df-4178-80b2-11170a346154">

4. AI-Bot response
<img width="1440" alt="Screenshot 2024-05-04 at 6 04 30 PM" src="https://github.com/github-cloudlabsuser-771/AI-Bytes-Smart-Swipe/assets/167456961/ab36d851-9e40-4a34-9303-c0970d64d7d9">

5. Profile
<img width="1440" alt="Screenshot 2024-05-04 at 6 04 55 PM" src="https://github.com/github-cloudlabsuser-771/AI-Bytes-Smart-Swipe/assets/167456961/f50f678f-56bd-4967-bf28-c5ec7f452ab4">

6. Dev Team
<img width="1440" alt="Screenshot 2024-05-04 at 6 05 15 PM" src="https://github.com/github-cloudlabsuser-771/AI-Bytes-Smart-Swipe/assets/167456961/744f67ab-fe50-4cfb-a83b-f9c41665afec">


Developed by - **Team AI Bytes** from Capgemini Pune, INDIA.