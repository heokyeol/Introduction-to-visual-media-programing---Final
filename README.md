# Final project : INeedHighCGPA
>This project referenced by [shumup!](https://kidscancode.org/blog/2016/09/pygame_shmup_part_10/)

## 1. Intro
>"I want to graduate..."
>
>"I Need A+..."
>
You can easily raise your CGPA with this game!

## 2. Game sequance
<img width="500" alt="스크린샷 2023-12-27 05 33 09" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/50c9d08b-a097-4a56-83bf-347a496fd6a0">

- When the score mobs hit core, CGPA changes and earned credit increases.
- When you earn every 130 credits, your highest education level renewals. 
- There is some clear sequance and over sequance,
  - **game clear (doctor graduate)**
    - earn 390 credit
  - **game over (Dismissal)**
    - player hitted by mob 10 times
    - get F score 5 times
- Not only clear, but also you have to care about CGPA
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
- But you can't erase the wall, so do not block A+ and press spacebar carefully!
- Or, you can diffence by eat the score by self, but that's cheeting. So your HP descreas. Do this only in emergency!


## 4. Components
| Player | CGPA display | Mobs(scores) | Block | 
|:---:|:---:|:---:|:---:|
|<img width="100" alt="스크린샷 2023-12-27 09 50 46" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/39057b63-7158-4ebf-81b3-f5f44338e1d8"> | <img width="100" alt="스크린샷 2023-12-27 09 50 58" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/91a40bcb-75ed-4413-84aa-2f2de73b2836"> | <img width="100" alt="스크린샷 2023-12-27 09 52 30" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/16e27cd3-e0e5-4b62-a3bf-794941f9b125"> | <img width="100" alt="스크린샷 2023-12-27 09 52 41" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/48618f7c-487f-465f-9d24-d4e30ab30439"> |


Except above components, I designed many pixel components for you.
>player icon motivated by *Panman*


<img width="200" alt="image" src="https://github.com/heokyeol/Introduction-to-visual-media-programing---Final/assets/70618615/98693834-9e4f-488a-97a4-67c46d80f782">

## 5. Code

```python
class posArray():
  #an array which controls ingame space
class Core(pygame.sprite.Sprite):
  #core monitor
class Player(pygame.sprite.Sprite):
  #player
class Cap(pygame.sprite.Sprite):
  #when you earn 130 credits, get 1 graduation cap,  260 credits, get 2 graduation cap.
class Wall(pygame.sprite.Sprite):
  #Hot6 drink, It blockes mobs and bother player's moving
class Mob(pygame.sprite.Sprite):
  #score mobs
class Tail(pygame.sprite.Sprite):
  #score mobs' tail effect animation
class Explosion(pygame.sprite.Sprite):
  #explosion effect animation
class Scored(pygame.sprite.Sprite):
  #scored effect animation
class introMob(Mob):
  #background component of intro, overriding Mob() class
```
- I made many functions, classes and algorithms for game.
  - but I'm embarrassed because there's many inefficient codes
  - but I'm proud about it works well
