# grabTT
## What it is and why you need it
grabTT is a solution software that aims at easing out the "additional/breadth subject" selection process in ERP. If you are not aware of the problem let me explain it to you -

1. First you need to open **FOUR seperate** tabs and keep juggling between them in the next steps to come - a. Timetable -> Central Timetable, b. Timetalbe -> DepartmentWise, c. Timetable ->Subject List with slots, d. Subjects -> Curriculum Syllabus details
2. From tab a, you find out where all slots are and draw it in your copy. Then from tab b, you find out what slots are occupied by your department and mark them on your copy. Then from tab c, you find out which subjects are left for you to take additionals. Then you go back to tab c and check for EACH department whose subjects you want to take as additional and mark its slots on your copy. 
3. What makes it more difficult is that you have to check subject and its prerequisites from tab d manually among a list of many subject. The horrendous complexity of the Central Timetable definitely adds to it.

## What my solution is
I have designed this GUI based software that eases the process out drastically -

1. The slots are already recorded and configured. You simply select one by one the subject you want and its respective slot. Whenever there is a slot clash the software automatically tells you. 
2. As a bonus at the end you get a sweet .png file of your routine, and a .ics file that you can add to your calendar.
3. The files are stored in easy and editable text formats, so you can edit everything about this with almost no coding knowledge.

## Areas to work on
In no way a conclusive list -
1. Design a web-based GUI for this for accesibility across all platforms.
2. Integrate it with erp login so that information about department and department subjects can be retrieved.
3. To retrieve list of subjects from ERP and make it available here.
