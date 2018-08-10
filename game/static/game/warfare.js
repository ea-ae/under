function setPage(data) { // Sets the data in the active tab
    if (data.page == active) { // Make sure we're sent the correct page
        if (data.page == 'home') {
            if ('cult' in data) { // Whether this user already has a cult
                document.querySelector('.tabs__home .stats').style.display = 'block';
                document.querySelector('.tabs__home .create-cult').style.display = 'none';

                document.querySelector('.tabs__home .username span').innerHTML = data.username;
                document.querySelector('.tabs__home .cult-name').innerHTML = data.cult.name;

                document.querySelector('.tabs__home .type .val').innerHTML = data.cult.type;
                document.querySelector('.tabs__home .money .val').innerHTML = '$' + data.cult.money;
                document.querySelector('.tabs__home .rep .val').innerHTML = data.cult.rep;
            } else {
                // Code to create a new cult
                document.querySelector('.tabs__home .stats').style.display = 'none';
                document.querySelector('.tabs__home .create-cult').style.display = 'block';
            }
        } else if (data.page == 'contacts') {
            console.debug(data.contacts);
            messages.contacts = data.contacts;
            // TODO: localStorage to remember last selected contact
            messages.setActiveContact(messages.contacts.anonymous);
        } else if (data.page == 'headquarters') {
            if (firstHQVisit) {
                firstHQVisit = false;
                var upgrades = document.getElementsByClassName('upgrade');
                for (var i = 0; i < upgrades.length; i++) {
                    upgrades[i].addEventListener('click', headquarters.selectUpgrade);
                }
            }
        } 
        // Show the tab's div now that all the data is set
        document.getElementsByClassName('tabs__' + data.page)[0].style.display = 'block';
    }
}

function setActiveTab(event, checkIfSame=true) {
    // Get pressed element's ID and extract the part after __
    var pid = event.target.getAttribute('id').split('__')[1];
    if (tabSwitchFinished && (active != pid || !checkIfSame)) {
        tabSwitchFinished = false;

        socket.send(JSON.stringify({
            type: 'page_data',
            page: pid
        }));

        // Remove 'active-tab' from previous active tab
        document.getElementById('tabs-list__' + active).classList.remove('active-tab');
        // Hide content from previous active tab
        document.getElementsByClassName('tabs__' + active)[0].style.display = 'none';
        // Add 'active-tab' to the clicked tab
        event.target.classList.add('active-tab');
        // Set clicked tab as the new active tab
        active = pid;

        setTimeout(function() {
            tabSwitchFinished = true;
        }, 200);
    }
}

var messages = {
    setActiveContact: function(contact) {
        var i;
        messages.selectedContact = contact.id;
        document.getElementsByClassName('contact-details__text')[0].innerHTML = contact.text;
        document.getElementsByClassName('contact-details__title')[0].innerHTML = contact.name;
        var optionsList = document.querySelector('.contact-details__options ul');
        optionsList.innerHTML = '';

        for (i = 0; i < contact.options.length; i++) {
            optionsList.innerHTML += '<li' +
            (contact.options[i].enabled ? '' : ' class="disabled-text"') +
            '>' + contact.options[i].text + '</li>';
        }

        for (i = 0; i < messages.options.length; i++) {
            messages.options[i].removeEventListener('click', messages.selectOption);
        }

        messages.options = [];

        for (i = 0; i < optionsList.children.length; i++) {
            messages.options.push(optionsList.children[i]);
            optionsList.children[i].addEventListener('click', messages.selectOption);
        }

        var img = document.getElementsByClassName('contact--' + contact.id)[0].children[0].children[0];
        document.querySelector('.contact-details__top img').src = img.src;
    },
    selectOption: function(e) { // Click handler
        socket.send(JSON.stringify({
            type: 'card_choice',
            contact: messages.selectedContact,
            choice: messages.options.indexOf(e.target)
        }));
    },
    selectedContact: 'anonymous',
    options: [],
    contacts: {
        // THE CONTACTS BELOW ARE MERELY EXAMPLES
        detective: {
            name: 'The Detective',
            id: 'detective',
            options: [{
                text: 'Consider it done.',
                enabled: true
            }, {
                text: 'Find someone else, we have other things to do.',
                enabled: true
            }],
            text: `
            <p>
                Hello, we have an individual that we need to get rid of. He knows that we
                are coming, so he has barricaded himself in his apartment. We know that he
                has a hidden camera at the front door and that he keeps a handgun with him
                at all times.
            </p>
            <p>
                His name is Jonathan Brease and he lives on the 6th floor of Gremlin Street 38,
                in apartment 72. I don't care how dirty you do the job, just do it fast. Are you in?
            </p>
            <p>
                <b>Objective:</b> Assassinate Jonathan Brease.
            </p>
            `
        },
        anonymous: {
            name: 'Anonymous',
            id: 'anonymous',
            options: [{
                text: 'I\'m ready, now what?',
                enabled: false
            }, {
                text: 'Tell me more.',
                enabled: true
            }],
            text: `
            <p>
                So, you're looking to start a cult? I'll help you
                get started. Don't worry about any payments for now,
                you'll return the favor when the time comes.
            </p>
            <p>
                First of all, you'll need a building for your cult to
                operate in. I found you a quiet place in the corner of
                the city, nobody should bother you there. Check it out
                and tell me once you're ready.
            </p>
            <p>
                <b>Objective:</b> Visit the headquarters using the
                sidebar and then return to this tab.
            </p>
            `
        },
        assistant: {
            name: 'The Assistant',
            id: 'assistant',
            options: [{
                text: 'Let\'s do it then - better safe than sorry (pay $9500).',
                enabled: true
            }, {
                text: 'Thanks for the suggestion, but that is not a priority right now.',
                enabled: true
            }],
            text: `
            <p>
                The police visited our headquarters today, due to several neighbor's complaints
                about the loud noises that are constantly being heard on our property. From
                the descriptions of the noise, it is quite clear that they were hearing us
                opening the portal to The Underworld.
            </p>
            <p>
                We should probably invest in a soundproof room for our Underworld portal to
                avoid further attention from the neighbors and police.
            </p>
            `
        },
        merchant: {
            name: 'The Merchant',
            id: 'merchant',
            options: [{
                text: 'I got you one.',
                enabled: false
            }, {
                text: 'Maybe another time.',
                enabled: true
            }],
            text: `
            <p>
                I have a customer who is in need of a hostile demon. He didn't tell me
                why, but knowing him, it's probably nothing good.
            </p>
            <p>
                <b>Objective:</b> Find a hostile 'Demon in a Bottle'.
            </p>
            `
        }
    }
};

var headquarters = {
    selected: null,
    selectUpgrade: function(e) {
        if (headquarters.selected !== null) {
            headquarters.selected.classList.remove('upgrade--selected');
            headquarters.selected.children[1].remove();
        }

        if (headquarters.selected !== this) {
            var btn = document.createElement('button');
            btn.innerHTML = 'Buy';
            this.appendChild(btn);

            this.classList.add('upgrade--selected');
            headquarters.selected = this;
        } else {
            headquarters.selected = null;
        }
    }
}

var connected = false,
    visible = true,
    animationFinished = true,
    tabSwitchFinished = true,
    firstHQVisit = true,
    active = 'home';

window.addEventListener('load', function() { // Once page loaded and parsed
    messages.setActiveContact(messages.contacts.anonymous);

    document.getElementsByClassName("contact--detective")[0].addEventListener('click', function() {
        messages.setActiveContact(messages.contacts.detective);
    });

    document.getElementsByClassName("contact--anonymous")[0].addEventListener('click', function() {
        messages.setActiveContact(messages.contacts.anonymous);
    });
    document.getElementsByClassName("contact--assistant")[0].addEventListener('click', function() {
        messages.setActiveContact(messages.contacts.assistant);
    });
    document.getElementsByClassName("contact--merchant")[0].addEventListener('click', function() {
        messages.setActiveContact(messages.contacts.merchant);
    });

    var ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
    var ws_path = ws_scheme + '://' + window.location.host + '/ws/warfare';
    socket = new ReconnectingWebSocket(ws_path, null, {
        debug: true,
		reconnectInterval: 500000,
        timeoutInterval: 5000,
        maxReconnectAttempts: 0
    });

    socket.onopen = function() {
        document.getElementsByClassName('spinner')[0].remove();
        connected = true; // Allow tab switching etc.

        // Set 'home' as the initial tab
        setActiveTab({target: document.getElementById('tabs-list__home')}, false);

        var tabs = document.querySelectorAll('.tabs-list li');
        for (var i = 0; i < tabs.length; i++) {
            tabs[i].addEventListener('click', setActiveTab);
        }
    }

    socket.onclose = function() {
        console.debug('WebSocket connection closed.');
    }

    socket.onerror = function(err) {
        console.error(err);
    }

    socket.onmessage = function(message) { // The consumer sends us a message
        var data = JSON.parse(message.data);
        if (data.type == 'page_data') {
            setPage(data); // We are sent data about a requested page
        } else if (data.type == 'page_redirect') { // Server wants to change the active tab
            setActiveTab({target: document.getElementById('tabs-list__' + data.page)});
        }
    }

    document.getElementById('create-cult__form').addEventListener('submit', function(e) {
        e.preventDefault(); // Don't submit the form, instead send it over websockets
        socket.send(JSON.stringify({
            type: 'create_cult',
            cult_data: {
                cult_name: document.getElementById('cult-name').value,
                cult_type: document.querySelector('input[name="cult-type"]:checked').value
            }
        }));

        // Redirect user to another page

        setActiveTab({target: document.getElementById('tabs-list__contacts')});
    });

    var hamburger = document.querySelector('nav .hamburger');
    hamburger.addEventListener('click', function() { // Open/close sidebar
        if (animationFinished) {

            animationFinished = false;
            this.classList.toggle('is-active'); // Toggles between two hamburger icons
            var tabs = document.querySelector('.sidebar');
            tabs.classList.toggle('sidebar--visible');


            if (visible) {
                tabs.style.marginLeft = '-' + (tabs.offsetWidth + 1) + 'px';
            } else {
                tabs.style.marginLeft = '0';
            }

            visible = !visible;
            setTimeout(function() {
                animationFinished = true;
            }, 360);
        }
    });

    window.onresize = function() {
        if (!visible) {
            var tabs = document.querySelector('.sidebar--visible');
            tabs.style.marginLeft = '-' + (tabs.offsetWidth + 1) + 'px';
        }
    };
});