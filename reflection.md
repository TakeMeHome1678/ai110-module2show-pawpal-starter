# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    initial design will focus on starting with creating a pet, then creating a task and sub task called care task, then allowing the caregivers and timeslots.
    classes are as follow:
    pet with fields that allow to detail the pets description, task with fields that allow to create modifications if needed, caretasks will details what type of tasks will be accomplished, while lastly caregivers and timeslots will allow to choose what fits the users preferences/needs.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    Yes there were a lot of changes as per AI *Gemini* the biggest one was task recurrence, becasue it would only allow one walk when pets may require two at minimum per day
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
it considers time availability, priority levels, task dependencies, flexibility & tolerance windows, household multi-pet scope.
saftey & health first so priority and time, dependecies, multi-pet allowing

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
 for tradeoffs there wasnt really much to do except tweak a bit of an algorithm already implemented with a small change that saved a few seconds.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
i used AI tools pretty much to help with every step process from brainstorming to debugging and checking for bugs. I believe the most helpful prompts were the ones from the tips and hints in codepath which allowed to check if my AI was actually choosing the best methods for coding.
**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
one time i didnt accept AI as-is was when it was asking to change code that was not even in the main code (app.py). I verified what it wanted it do by questioning why it was choosing that code and how can it be changed without changing unecesary codes.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
i tested most common behaviors that one would expect to run, i did not test for edge cases for the purpose of my testing first was for usability rather than security. These tests were important because it would defeat of creating an app with basic errors when deployed and having to submit update with batches back to back leading to user backlash for usability and then security. 
**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
i give it a strong four that it works correctly. 
i would test for overoutput like if the user can see more information than needed both the caregiver and pet owner. then i would test for exposure and see what can be taken advantage to escalate their privileges to gain access to admin power. 
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
i was satisifed with how well AI was able to determine stuff for me without even me asking to or even yet thinking of it.
**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve the user interface to make it more enganging with friends and family allowing for communities to grow wihtin the app. 
**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
That despite how fast, precise, and able to look into the future problems there will always be hiccups and reminds me why engineers need to supervise and test all. This creates the need for human to make the last call on code not AI, make sure things work as they are suppsoed to no less and no more. 
