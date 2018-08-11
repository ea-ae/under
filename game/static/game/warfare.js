// Shortcut function names
let getByClass = function(className) { return document.getElementsByClassName(className); }
let getById = function(id) { return document.getElementById(id); }
let getByQuery = function(query) { return document.querySelector(query); }

function setPage(data) { // Sets the data in the active tab
    if (data.page != active) { // Make sure we're sent the correct page
        return False;
    } 
    if (data.page == 'home') {
        if ('cult' in data) { // Whether this user already has a cult
            getByQuery('.tabs__home .stats').style.display = 'block';
            getByQuery('.tabs__home .create-cult').style.display = 'none';

            getByQuery('.tabs__home .username span').innerHTML = data.username;
            getByQuery('.tabs__home .cult-name').innerHTML = data.cult.name;
            getByQuery('.tabs__home .type .val').innerHTML = data.cult.type;
            getByQuery('.tabs__home .rep .val').innerHTML = data.cult.rep;
            let money = currency.format(data.cult.money);
            getByQuery('.tabs__home .money .val').innerHTML = money;
            getByQuery('.tabs__headquarters .money').innerHTML = 'Balance: ' + money;
            //getByQuery('.nav__money').innerHTML = currency.format(data.cult.money);
        } else {
            // Code to create a new cult
            getByQuery('.tabs__home .stats').style.display = 'none';
            getByQuery('.tabs__home .create-cult').style.display = 'block';
        }
    } else if (data.page == 'contacts') {
        messages.contacts = data.contacts;
        // TODO: localStorage to remember last selected contact
        messages.setActiveContact(messages.selectedContact);
    } else if (data.page == 'headquarters') {
        if (firstHQVisit) {
            firstHQVisit = false;
            let upgrades = getByClass('upgrade');
            for (let i = 0; i < upgrades.length; i++) {
                upgrades[i].addEventListener('click', headquarters.selectUpgrade);
            }
        }

        for (let i = 0; i < data.upgrades.length; i++) {
            getByClass('upgrade--' + data.upgrades[i])[0].classList.add('upgrade--owned');
        }
    } 
    // Show the tab's div now that all the data is set
    getByClass('tabs__' + data.page)[0].style.display = 'block';
    // Some after-display code
    if (data.page == 'headquarters') {
        let wrapper = getByClass('headquarters__details__wrapper')[0];
        console.log(wrapper.offsetHeight);
        wrapper.style.minHeight = wrapper.offsetHeight + 'px';
    }
}

function setActiveTab(event, checkIfSame=true) {
    // Get pressed element's ID and extract the part after __
    let pid = event.target.getAttribute('id').split('__')[1];
    if (tabSwitchFinished && (active != pid || !checkIfSame)) {
        tabSwitchFinished = false;

        socket.send(JSON.stringify({
            type: 'page_data',
            page: pid
        }));

        // Remove 'active-tab' from previous active tab
        getById('tabs-list__' + active).classList.remove('active-tab');
        // Hide content from previous active tab
        getByClass('tabs__' + active)[0].style.display = 'none';
        // Add 'active-tab' to the clicked tab
        event.target.classList.add('active-tab');
        // Set clicked tab as the new active tab
        active = pid;

        setTimeout(function() {
            tabSwitchFinished = true;
        }, 200);
    }
}

let messages = {
    selectedContact: 'anonymous',
    options: [],
    setActiveContact: function(contact) {
        let i;
        console.log(contact);
        contact = messages.contacts[contact];
        messages.selectedContact = contact.id;
        getByClass('contact-details__text')[0].innerHTML = contact.text;
        getByClass('contact-details__title')[0].innerHTML = contact.name;
        let optionsList = getByQuery('.contact-details__options ul');
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

        let img = getByClass('contact--' + contact.id)[0].children[0].children[0];
        getByQuery('.contact-details__top img').src = img.src;
    },
    selectOption: function(e) { // Click handler
        socket.send(JSON.stringify({
            type: 'card_choice',
            contact: messages.selectedContact,
            choice: messages.options.indexOf(e.target)
        }));
    },
    contacts: {
        anonymous: {
            name: 'Anonymous',
            id: 'anonymous',
            options: [{
                text: 'Loading...',
                enabled: false
            }],
            text: '<p>Loading...</p>'
        },
    }
};

let headquarters = {
    selected: null,
    btn: null,
    selectUpgrade: function(e) {
        if (headquarters.selected !== null) {
            headquarters.btn.removeEventListener('click', headquarters.buyUpgrade);
            headquarters.selected.classList.remove('upgrade--selected');
            headquarters.selected.children[1].remove();
        }

        if (headquarters.selected !== this) {
            let btn = document.createElement('button');

            if (this.classList.contains('upgrade--owned')) {
                btn.innerHTML = 'Delete';
            } else {
                btn.innerHTML = 'Buy';
            }

            btn.addEventListener('click', headquarters.manageUpgrade);
            this.appendChild(btn);
            headquarters.btn = btn;

            this.classList.add('upgrade--selected');
            headquarters.selected = this;
            headquarters.setData(headquarters.upgrades[this.classList[1].split('--')[1]]);
        } else {
            headquarters.selected = null;
            headquarters.setData({
                name: 'Select an upgrade',
                id: 'none',
                cost: 0,
                description: '<p>Select an upgrade to view more information about it.</p> \
                <p>You can only have a limited amount of upgrades at a time.</p> \
                <p>If you delete an upgrade, you do not get your money back.</p>'
            });
        }
    },
    manageUpgrade: function(e) { // Buy or sell an upgrade
        let upgradeDiv = this.parentElement;
        if (this.parentElement.classList.contains('upgrade--owned')) {
            alerty.confirm('Are you sure you want to delete this upgrade?\n \
            You cannot revert this!', {
                title: 'Confirmation',
                okLabel: 'Yes',
                cancelLabel: 'No'
            }, function() {
                socket.send(JSON.stringify({
                    type: 'hq_upgrade',
                    command: 'delete',
                    item: upgradeDiv.classList[1].split('--')[1]
                }));

                upgradeDiv.classList.remove('upgrade--owned');

                alerty.toasts('Upgrade deleted!', {
                    bgColor: '#35444e',
                    fontColor: '#fefefe',
                    time: 4000
                });
            });
        } else {
            let money = getByQuery('.tabs__headquarters .money').innerHTML.substring(10);
            money = parseInt(money.split(',').join(''));
            let upgradeCost = 
                headquarters.upgrades[headquarters.selected.classList[1].split('--')[1]].cost;

            if (upgradeCost > money) {
                alerty.alert('You do not have enough money!', {
                    title: 'Oops!',
                    okLabel: 'OK'
                })

                return false;
            }

            alerty.confirm('Are you sure you want to buy this upgrade?', {
                title: 'Confirmation',
                okLabel: 'Yes',
                cancelLabel: 'No'
            }, function() {
                socket.send(JSON.stringify({
                    type: 'hq_upgrade',
                    command: 'buy',
                    item: upgradeDiv.classList[1].split('--')[1]
                }));

                upgradeDiv.classList.add('upgrade--owned');

                getByQuery('.tabs__headquarters .money').innerHTML = 
                    'Balance: ' + currency.format(money - upgradeCost);

                alerty.toasts('Upgrade bought!', {
                    bgColor: '#35444e',
                    fontColor: '#fefefe',
                    time: 4000
                });
            });
        }
    },
    setData: function(upgrade) { // Fill in the detail text spots
        getByQuery('.headquarters__details h2').innerHTML = upgrade.name;
        getByQuery('.stats__data .cost').innerHTML = currency.format(upgrade.cost);
        getByQuery('.stats__text').innerHTML = '<p>' + upgrade.description + '</p>';
    },
    upgrades: {
        'windowbars': {
            'name': 'Window Security Bars',
            'id': 'windowbars',
            'cost': 2500,
            'description': 'Prevent intruders from entering through the windows - unless they have a metal cutter.'
        },
        'motionsensors': {
            'name': 'Motion Sensors',
            'id': 'motionsensors',
            'cost': 5000,
            'description': 'Detect movement in unauthorized areas. Keep in mind that experienced thiefs have methods for getting past them.'
        },
        'cctv': {
            'name': 'CCTV System',
            'id': 'cctv',
            'cost': 7500,
            'description': 'Set up security cameras around the area. You will need guards to monitor the cameras, though.'
        },
        'ups': {
            'name': 'Uninterruptible Power Supply',
            'id': 'ups',
            'cost': 10000,
            'description': 'An emergency power supply in case the power goes out for any reason.'
        },
        'insurance': {
            'name': 'Insurance',
            'id': 'insurance',
            'cost': 25000,
            'description': 'In case of a successful burglary, you get back 10% of money lost.'
        },
        'doorsystem': {
            'name': 'Door Access Control System',
            'id': 'doorsystem',
            'cost': 75000,
            'description': 'All employees are given keycards that are used to open doors. Even though it makes a lockpicker useless, a technician could bypass it easily.'
        },
        'jammers': {
            'name': 'Signal Jammers',
            'id': 'jammers',
            'cost': 100000,
            'description': 'Block any incoming signals to protect against hackers.'
        },
        'fencing': {
            'name': 'Perimeter Fencing',
            'id': 'fencing',
            'cost': 125000,
            'description': 'Barbed wire metal fences that circle the perimeter to prevent unauthorized property access.'
        },
        'lockdownsystem': {
            'name': 'Emergency Lockdown System',
            'id': 'lockdownsystem',
            'cost': 150000,
            'description': 'In case of a detected intrusion, block all doors and windows from opening.'
        }
    },
}

let currency = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
}),
    connected = false,
    visible = true,
    animationFinished = true,
    tabSwitchFinished = true,
    firstHQVisit = true,
    active = 'home',
    socket;

window.addEventListener('load', function() { // Once page loaded and parsed
    // Shortcut function names again, cause who cares
    let getByClass = function(className) { return document.getElementsByClassName(className); }
    let getById = function(id) { return document.getElementById(id); }
    let getByQuery = function(query) { return document.querySelector(query); }

    messages.setActiveContact('anonymous');

    getByClass("contact--mafioso")[0].addEventListener('click', function() {
        messages.setActiveContact('mafioso');
    });

    getByClass("contact--anonymous")[0].addEventListener('click', function() {
        messages.setActiveContact('anonymous');
    });
    getByClass("contact--assistant")[0].addEventListener('click', function() {
        messages.setActiveContact('assistant');
    });
    getByClass("contact--merchant")[0].addEventListener('click', function() {
        messages.setActiveContact('merchant');
    });

    let ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws',
        ws_path = ws_scheme + '://' + window.location.host + '/ws/warfare',
        hamburger = getByQuery('nav .hamburger');
    
    socket = new ReconnectingWebSocket(ws_path, null, {
        debug: true,
		reconnectInterval: 500000,
        timeoutInterval: 5000,
        maxReconnectAttempts: 0
    });

    socket.onopen = function() {
        console.log(getByClass('spinner'));
        getByClass('spinner')[0].remove();
        connected = true; // Allow tab switching etc.

        // Set 'home' as the initial tab
        setActiveTab({target: getById('tabs-list__home')}, false);

        let tabs = document.querySelectorAll('.tabs-list li');
        for (let i = 0; i < tabs.length; i++) {
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
        let data = JSON.parse(message.data);
        if (data.type == 'page_data') {
            setPage(data); // We are sent data about a requested page
        } else if (data.type == 'page_redirect') { // Server wants to change the active tab
            setActiveTab({target: getById('tabs-list__' + data.page)});
        }
    }

    getById('create-cult__form').addEventListener('submit', function(e) {
        e.preventDefault(); // Don't submit the form, instead send it over websockets
        socket.send(JSON.stringify({
            type: 'create_cult',
            cult_data: {
                cult_name: getById('cult-name').value,
                cult_type: getByQuery('input[name="cult-type"]:checked').value
            }
        }));

        // Redirect user to another page

        setActiveTab({target: getById('tabs-list__contacts')});
    });

    getByClass('nav__logout')[0].addEventListener('click', function() {
        alerty.confirm('Are you sure you want to log out?', {
            title: 'Confirmation',
            okLabel: 'Yes',
            cancelLabel: 'No'
        }, function() {
            window.location.replace('../logout');
        });
    });

    hamburger.addEventListener('click', function() { // Open/close sidebar
        if (animationFinished) {

            animationFinished = false;
            this.classList.toggle('is-active'); // Toggles between two hamburger icons
            let tabs = getByQuery('.sidebar');
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
            let tabs = getByQuery('.sidebar--visible');
            tabs.style.marginLeft = '-' + (tabs.offsetWidth + 1) + 'px';
        }
    };
});