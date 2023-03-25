document.addEventListener('DOMContentLoaded', () => {
    let ref1 = document.querySelector(".ref1").value;
    setTimeout(() => {
        fetch(`/flight/ticket/api/${ref1}`)
        .then(response => response.json())
        .then(ticket1 => {
            if (ticket1.status === 'CONFIRMED') {
                document.querySelector(".section2 .flight1 .ref").innerText = ticket1.ref;
                document.querySelector(".section2 .flight1 .from1").innerText = ticket1.from;
                document.querySelector(".section2 .flight1 .to1").innerText = ticket1.to;
            }
            else {
                throw Error(ticket1.status);
            }
        })
        .then(() => {
            document.querySelector(".section1").style.display = 'none';
            document.querySelector(".section2").style.display = 'block';
            document.querySelector(".section3").style.display = 'none';
            //document.querySelector(".section2 svg").style.animationPlayState = 'running';
        })
        .catch(() => {
            document.querySelector(".section1").style.display = 'none';
            document.querySelector(".section2").style.display = 'none';
            document.querySelector(".section3").style.display = 'block';
        })
    }, 2000);
})