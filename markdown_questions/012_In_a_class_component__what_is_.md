---
difficulty: 1
tags: Basics of React, State
---

In a class component, what is the proper syntax to update the following default  state to [b]{name: "Joe"}[/b]:


[code]this.state = {name: ""};[/code]


[code]this.setName("Joe");[/code]


[code]this.setState("Joe");[/code]

#
[code]this.setState({name: "Joe"});[/code]


[code]this.state.name = "Joe";[/code]

