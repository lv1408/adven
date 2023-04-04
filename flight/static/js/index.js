document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#adven-from").addEventListener("input", event => {
        adven_from(event);
    });

    document.querySelector("#adven-to").addEventListener("input", event => {
        adven_to(event);
    });

    document.querySelector("#adven-from").addEventListener("focus", event => {
        adven_from(event, true);
    });

    document.querySelector("#adven-to").addEventListener("focus", event => {
        adven_to(event, true);
    });

    document.querySelectorAll('.trip-type').forEach(type => {
        type.onclick = trip_type;
    });

});


function showplaces(input) {
    let box = input.parentElement.querySelector(".places_box");
    box.style.display = 'block';
}

function hideplaces(input) {
    let box = input.parentElement.querySelector(".places_box");
    setTimeout(() => {
        box.style.display = 'none';
    }, 300);
}

function selectplace(option) {
    let input = option.parentElement.parentElement.querySelector('input[type=text]');
    input.value = option.dataset.value.toUpperCase();
    input.dataset.value = option.dataset.value;
}

function adven_to(event, focus=false) {
    let input = event.target;
    let list = document.querySelector('#places_to');
    showplaces(input);
    if(!focus) {
        input.dataset.value = '';
    }
    if(input.value.length > 0) {
        fetch('query/places/'+input.value)
        .then(response => response.json())
        .then(places => {
            list.innerHTML = '';
            places.forEach(element => {
                let div = document.createElement('div');
                div.setAttribute('class', 'each_places_to_list');
                div.classList.add('places__list');
                div.setAttribute('onclick', "selectplace(this)");
                div.setAttribute('data-value', element.code);
                div.innerText = `${element.city} (${element.country})`;
                list.append(div);
            });
        });
    }
}

function adven_from(event, focus=false) {
    let input = event.target;
    let list = document.querySelector('#places_from');
    showplaces(input);
    if(!focus) {
        input.dataset.value = '';
    }
    if(input.value.length > 0) {
        fetch('query/places/'+input.value)
        .then(response => response.json())
        .then(places => {
            list.innerHTML = '';
            places.forEach(element => {
                let div = document.createElement('div');
                div.setAttribute('class', 'each_places_from_list');
                div.classList.add('places__list');
                div.setAttribute('onclick', "selectplace(this)");
                div.setAttribute('data-value', element.code);
                div.innerText = `${element.city} (${element.country})`;
                list.append(div);
            });
        });
    }
}

function trip_type() {
    document.querySelectorAll('.trip-type').forEach(type => {
        if(type.checked) {
            if(type.value === "1") {
                document.querySelector('#return_date').disabled = false;
            }
            else if(type.value === "2") {
                document.querySelector('#return_date').disabled = false;
            }
        }
    })
}

function adven_search() {
    if(!document.querySelector("adven-from").dataset.value) {
        alert("Please select your home city.");
        return false;
    }
    if(!document.querySelector("#adven-to").dataset.value) {
        alert("Please select your destination city.");
        return false;
    }
}