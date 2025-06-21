# lemin captcha solver
only supporting single piece challenge, and the image solver is skidded and not good you should make it by yourself :(
# usage
```py
import lemin

lemin_solved = lemin.solve("CROPPED_9933778_1cb25070c75540bf8f4bf3ca0c4f1ffb")
lemin_solved["answer"] # "0xaxcgx0xaxc6x0xaxbsx...D3s1X" or "Failed"
lemin_solved["captcha_id"] # "8d95b4c0-41f3-4dd9-b527-0fbad8429e35"
```
