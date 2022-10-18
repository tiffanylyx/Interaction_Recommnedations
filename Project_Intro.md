# Suggesting interaction behaviors based on visual states and interaction sequence in temporal-spatial trajectory data

## Paper Link
[paper link](https://www.overleaf.com/5393329791gvnpnnchbcfp)
## Introduction

### Background

1. Data visualization has become an essential tool of public education organizations that provide informal learners an opportunity to engage with critical new areas of knowledge.

2. Interactions during the usage of visualization help the visitors to explore the data and obtain insights, which contribute to visitors’ engagements and can highly influences visitors' overall experience of the visualization and exhibition.[1]

3. Due to the speciality faced by museums and other public education organizations ( such as broad audience source, limited visiting time and competitions with other exhibits), interaction techniques for museum information visualizations should be as lightweight and intuitive as possible and also, it may be more important for the interaction design to imply or suggest possible next interactions.[2]


### Research Problem

1. How to model and encode users’ interaction behaviors and the corresponding visualization results (or visual states)

2. How to generate interaction suggestions during the data exploration process of future visitors based on the interaction paths collected from previous users

## Related Work

### Model Interaction Behaviours

1. J. S. Yi et. al classified interaction behaviours into 7 categories : select, to mark items of interest; explore, to examine a different subset of data; reconfigure, to show a different arrangement of data; encode, to use a different visual encoding; abstract/elaborate, to show more or less detail; filter, to show something conditionally; and, connect, to show related items.[3]

2. A. Satyanarayan et. al brought up an extension to Vega as a Declarative interaction design for data visualization, which used Json fromat to defined interaction behaviours under the taxonomy of J. S. Yi's work at 2014.[4]

3. A. Satyanarayan et. al developed Vega-lite, A Grammar of Interactive Graphics to defined interaction behaviours (which also provides elegant log information).[5]

### Generate Interaction Suggestions

1. F. Dabek and J. J. Caban developed A Grammar-based Approach for Modeling User Interactions and Generating Suggestions During the Data Exploration Process using K-Reversible algorithm on prefix tree acceptor.[6]

## Challanges and Solutions

### How to collect training data?

I. What’s the data?
The travel experience and creation content of 147 ancient Chinese literati from 搜韵-唐宋文学编年地图 (正在向版权方获得申请，等到拿到正式数据需要对数据格式进行定义，现在使用的数据是下载了网页源代码并自行清洗获得)

II. How to collect?
1. 从实验室同学
2. 众包
3. “虚拟博物馆”（可以结合PVis Contest）

### How to construct data structure (log interaction behaviours and visual states together)
1. We will use Vega-lite to structure visual system and log the changes of signals during the exploration process
2. We will capture and encode the visual states based on the view-type.

### What is the base of the prediction/suggestion

1. suggest interaction behaviors from current visualization state (suggest a from q1)
2. suggest interaction behaviors from previous interaction paths (suggest a from {bb})
3. suggest interaction behaviors from interaction paths + visualization states (suggest a from {q, a, q1, b, q4} 

## Reference

[1] J. Ma, K. -L. Ma and J. Frazier, "Decoding a Complex Visualization in a Science Museum – An Empirical Study," in IEEE Transactions on Visualization and Computer Graphics. (2020)

[2] U. Hinrichs, H. Schmidt and S. Carpendale, "EMDialog: Bringing Information Visualization into the Museum," in IEEE Transactions on Visualization and Computer Graphics. (2008)

[3] J. S. Yi, Y. a. Kang, J. Stasko and J. A. Jacko, "Toward a Deeper Understanding of the Role of Interaction in Information Visualization," in IEEE Transactions on Visualization and Computer Graphics. (2007)

[4] A. Satyanarayan, K. Wongsuphasawat and J. Heer, "Declarative interaction design for data visualization", Proceedings of the 27th annual ACM symposium on User interface software and technology. (2014)

[5] A. Satyanarayan, D. Moritz, K. Wongsuphasawat and J. Heer, "Vega-Lite: A Grammar of Interactive Graphics," in IEEE Transactions on Visualization and Computer Graphics. (2017)

[6] F. Dabek and J. J. Caban, "A Grammar-based Approach for Modeling User Interactions and Generating Suggestions During the Data Exploration Process,” in IEEE Transactions on Visualization and Computer Graphics (2017)
