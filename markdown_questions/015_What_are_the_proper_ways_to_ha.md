---
difficulty: 1
tags: Basics of React, JSX
---

What are the proper ways to have two sibling [b]div [/b]elements rendered by a React component [b]SayHello[/b]?


[code]function SayHello(props) {
   return (
         <div>Hello {props.name}</div>
         <div>Looking sharp today!</div>
   );
}[/code]

#
[code]function SayHello(props) {
     return (
       <>
            <div>Hello {props.name}</div>
            <div>Looking sharp today!</div>
        </>
    );
}[/code]

#
[code]function SayHello(props) {
     return (
       <React.Fragment>
            <div>Hello {props.name}</div>
            <div>Looking sharp today!</div>
        </React.Fragment>
    );
}[/code]


[code]function SayHello(props) {
     return (
       <React.Siblings>
            <div>Hello {props.name}</div>
            <div>Looking sharp today!</div>
        </React.Siblings>
    );
}[/code]

