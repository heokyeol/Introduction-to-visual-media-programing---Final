# Final project : INeedHighCGPA
>본 코드는 [shumup!](https://kidscancode.org/blog/2016/09/pygame_shmup_part_10/) 의 코드와 문서를 참고하여 제작하였음

## 1. Intro
>"I want to graduate..."
>
>"I Need A+..."
>
You can easily raise your CGPA with this game!

## 2. Game sequance
<img width="500" alt="스크린샷 2023-12-27 05 33 09" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/50c9d08b-a097-4a56-83bf-347a496fd6a0">


- There is some clear sequance and over sequance,
  - **game clear (doctor graduate)**
    - earn 390 credit
  - **game over (Dismissal)**
    - player hitted by mob 10 times
    - get F score 5 times
- Not only clear, you have to care about CGPA
  >*IF you graduate with low CGPA, you can't even get a job!*

## 3. How to raise *CGPA*

<img width="500" alt="스크린샷 2023-12-27 09 18 54" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/028adfcf-d0f3-430e-a0fe-e9aeb33e49ac">

- Your objective is increasing your *CGPA*, which displayed on center
- If the score mobs collepce with center monitor, your *CGPA* changes
  - A+ will highly increase *CGPA*
  - B will give small increase or decrease
  - F will give big big dessrease
- So, you have to block low scores!
  
  <img width="200" alt="스크린샷 2023-12-27 09 36 31" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/30d8d9e5-89d6-433d-aa73-68fd431e367d">

- Or, you can diffence by eat the score by self, but that's cheeting. So your HP descreas. Do this only in emergency!


## 4. Components
| Player | CGPA display | Mobs(scores) | Block | 
|:---:|:---:|:---:|:---:|
|<img width="100" alt="스크린샷 2023-12-27 09 50 46" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/39057b63-7158-4ebf-81b3-f5f44338e1d8"> | <img width="100" alt="스크린샷 2023-12-27 09 50 58" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/91a40bcb-75ed-4413-84aa-2f2de73b2836"> | <img width="100" alt="스크린샷 2023-12-27 09 52 30" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/16e27cd3-e0e5-4b62-a3bf-794941f9b125"> | <img width="100" alt="스크린샷 2023-12-27 09 52 41" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/48618f7c-487f-465f-9d24-d4e30ab30439"> |


Except above components, I designed many pixel components for you.
>player icon motivated by *Panman*


<img width="200" alt="image" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/98693834-9e4f-488a-97a4-67c46d80f782">

