![header](pics/header.png)
# Title
**project** is a 
---
---

# **Link to the web application** click [here](http://)


Content incudes:

* [Technologies](#technologies)

* [App Development](#app-development)

* [App Demo](#app-demo)

* [Contributors](#contributors)

---

## Technologies
>This project leverages python 3.7

* [Streamlit](https://streamlit.io/) - Deploy application into shareable web app

* [Dataclasses](https://docs.python.org/3/library/dataclasses.html) - Use the decorator and functions to generate methods automatically

* [Typing](https://docs.python.org/3/library/typing.html) - Provides runtime support for type hints

* [Datetime](https://docs.python.org/3/library/datetime.html) - Supplies classes for date and time manipulations

* [Pandas](https://pandas.pydata.org/) - Data analysis and manipulation

* [Hashlib](https://docs.python.org/3/library/hashlib.html) - Implements a common interface to different secure hash and message digest algorithms

---

## App Development
Create 3 dataclasses: 
* Class Record: defines inpute data and its type
* Class Block: process and encode inpute data to create a hash for blocks
* Class PyChain: defines difficulties, add each block, and validate the entire blockchain

Streamlit deployemt:
Designs and deploy app application

---

## App Demo

Go to the file folder contains pychian.py file and 

**Run application using command line** under the virtual environment contains all necessary dependencies

```python
streamlit run pychain.py
```

![commandline](pics/commandline.png)

---


**Input Data and add to blockchain**

![1](pics/1.png)

---

**Record each transaction**

As the Block Difficulty increased from 2 to 4, it took the nonce increased significantly.

![2](pics/2.png)
![3](pics/3.png)

---
**Block Inspector displays selected block information**

![4](pics/4.png)

---

**Chain validation shows the blockchain is safe and trustworthy**

![5](pics/5.png)

---


## Contributors

**Yanjun Lin Andrie** <span>&nbsp;&nbsp;</span> |
<span>&nbsp;&nbsp;</span> email: yanjun.lin.andrie@gmail.com <span>&nbsp;&nbsp;</span>|
<span>&nbsp;&nbsp;</span> [<img src="pics/linkedin.png" alt="in" width="20"/>](https://www.linkedin.com/in/yanjun-linked/)

**UC Berkeley Extension**

---

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
