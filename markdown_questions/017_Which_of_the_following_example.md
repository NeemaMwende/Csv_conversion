---
difficulty: 1
tags: Basics of React, Javascript
---

Which of the following examples are proper ways to call this function:


[code]function displayCar({make, model}) {
      console.log("Car: ", make, model);
}[/code]

#
[code]displayCar({make: "Tesla", model: "Cybertruck"});[/code]


[code]displayCar("Tesla", "Cybertruck");[/code]

#
[code]let car = {make: "Tesla", model: "Cybertruck"};
displayCar(car);[/code]


[code]displayCar(make: "Tesla", model: "Cybertruck");[/code]

