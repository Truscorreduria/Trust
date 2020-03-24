class Person {
    constructor(name) {
        this.name = name
    }

    say_hi() {
        console.log(`Hello i am ${this.name}`)
    }
}

class Developer extends Person {
    constructor(name) {
        super(name)
    }

    say_hi() {
        console.log(`$(i).am( ${this.name} )`)
    }
}


const a = new Person("cesar");

const b = new Developer("cesar");

a.say_hi();
b.say_hi();


(async function load() {
    async function llamarPersonaje(id) {
        const response = await fetch(`https://swapi.co/api/people/${id}`)
        const data = await response.json();
        console.log(data.name)
    }

    llamarPersonaje(2)
    llamarPersonaje(3)
    llamarPersonaje(1)
})()