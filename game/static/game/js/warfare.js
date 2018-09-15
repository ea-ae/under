// Shortcut function names
let getByClass = function(className) { return document.getElementsByClassName(className); };
let getById = function(id) { return document.getElementById(id); };
let getByQuery = function(query) { return document.querySelector(query); };

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

function setPage(data) { // Sets the data in the active tab
    if (data.page != active) { // Make sure we're sent the correct page
        return false;
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
        } else {
            // Code to create a new cult
            getByQuery('.tabs__home .stats').style.display = 'none';
            getByQuery('.tabs__home .create-cult').style.display = 'block';
        }
    } else if (data.page == 'contacts') {
        contacts.contacts = data.contacts;
        // TODO: localStorage to remember last selected contact
        contacts.setActiveContact(contacts.selectedContact);
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
    } else if (data.page == 'members') {
        if (firstMembersVisit) {
            firstMembersVisit = false;
            getByClass('tabs__info')[0].addEventListener('click', members.selectTab);
            getByClass('tabs__jobs')[0].addEventListener('click', members.selectTab);
            getByClass('tabs__learn')[0].addEventListener('click', members.selectTab);
            getByClass('tabs__manage')[0].addEventListener('click', members.selectTab);
            
            getByClass('promote-recruit')[0].addEventListener('click', members.promoteMember);
            getByClass('kick-recruit')[0].addEventListener('click', members.kickMember);
        }
        members.drawTree(data.members, data.recruit, data.jobs);
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

function deleteOverlays() {
    // There is a bug in Alerty that makes an overlays not delete themselves.
    // We can delete the alerty overlays by ourselves instead.
    let overlays = getByClass('alerty-overlay');
    for (let i = 0; i < overlays.length; i++) {
        overlays[i].remove();
    }
}

let chat = {
    setActiveMenuTab: function(e) {
        let menuList = getByClass('menu__list')[0].children;
        if (this == menuList[0]) { // Select sidebar
            menuList[1].classList.remove('active');
            menuList[0].classList.add('active');

            getByClass('sidebar__chat')[0].style.display = 'none';
            getByClass('sidebar__tabs')[0].style.display = 'block';
        } else { // Select chat
            menuList[0].classList.remove('active');
            menuList[1].classList.add('active');

            // I don't care at this point
            // CSS, you can go to hell
            let sidebarWidth = getByClass('sidebar')[0].offsetWidth;
            let screenHeight = document.documentElement.clientHeight;

            getByClass('sidebar__tabs')[0].style.display = 'none';
            getByClass('sidebar__chat')[0].style.display = 'block';

            let otherHeight = getByQuery('nav').offsetHeight + 40 + 
                getByQuery('.menu__list').offsetHeight +
                getByQuery('.chat__input').offsetHeight;

            getByClass('sidebar__chat')[0].style.width = sidebarWidth + 'px';
            getByClass('chat__text')[0].style.height = 
                (screenHeight - otherHeight) + 'px';
        }
    }
};

let contacts = {
    selectedContact: 'anonymous',
    options: [],
    displayContactList: function() {
        getByClass('contacts')[0].innerHTML = '';
        for (let key in contacts.contacts) {
            let div = document.createElement('div');
            let wrapper = document.createElement('div');
            let img = document.createElement('img');
            div.appendChild(wrapper);
            wrapper.appendChild(img);
            div.classList.add('contact');
            div.classList.add('contact--' + key);
            div.addEventListener('click', function() {
                contacts.setActiveContact(key);
            });
            wrapper.classList.add('contact__wrapper');
            img.setAttribute('src', IMAGES_URL + 'avatar-' + key + '.png');
            getByClass('contacts')[0].appendChild(div);
        }
    },
    setActiveContact: function(contact) {
        contacts.displayContactList();
        let i;
        contact = contacts.contacts[contact];
        contacts.selectedContact = contact.id;
        getByClass('contact-details__text')[0].innerHTML = contact.text;
        getByClass('contact-details__title')[0].innerHTML = contact.name;
        let optionsList = getByQuery('.contact-details__options ul');
        optionsList.innerHTML = '';
        for (i = 0; i < contact.options.length; i++) {
            optionsList.innerHTML += '<li' +
            (contact.options[i].enabled ? '' : ' class="disabled-text"') +
            '>' + contact.options[i].text + '</li>';
        }

        for (i = 0; i < contacts.options.length; i++) {
            contacts.options[i].removeEventListener('click', contacts.selectOption);
        }

        contacts.options = [];

        for (i = 0; i < optionsList.children.length; i++) {
            contacts.options.push(optionsList.children[i]);
            optionsList.children[i].addEventListener('click', contacts.selectOption);
        }
        let img = getByClass('contact--' + contact.id)[0].children[0].children[0];
        getByQuery('.contact-details__top img').src = img.src;
    },
    selectOption: function(e) { // Click handler
        if (!this.classList.contains('disabled-text')) {
            socket.send(JSON.stringify({
                type: 'card_choice',
                contact: contacts.selectedContact,
                choice: contacts.options.indexOf(e.target)
            }));
        }
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

let members = {
    chartMembers: null,
    memberSelected: null,
    jobList: null,
    firstTreeRender: true,
    drawTree: function(memberList, recruit, jobList) {
        members.jobList = jobList;
        if (!members.firstTreeRender) {
            members.firstTreeRender = false;
        }

        let config = {
            container: '#members__tree',
            connectors: {
                type: 'step',
                style: {
                    'stroke': 'rgb(143, 156, 161)', // 'rgb(127, 139, 143)',
                    'stroke-opacity': 1,
                    'stroke-width': 1.25,
                    'opacity': 1,
                    'fill-opacity': 1,
                    'stroke-linejoin': 'round'
                }
            },
            levelSeparation: 20, // px between node levels
            siblingSeparation: 10, // px between sibling nodes
            padding: 35
        };

        members.chartMembers = {
            '-1': {
                HTMLclass: '-1',
                text: {
                    name: 'You',
                    title: 'Leader'
                }
            }
        };

        let chart_config = [config, members.chartMembers['-1']];

        // Add all members to the chartMembers array in the correct format

        for (let i = 0; i < memberList.length; i++) {
            members.chartMembers[memberList[i].id] = {
                i: i,
                HTMLclass: memberList[i].id,
                text: {
                    name: memberList[i].name,
                    title: memberList[i].spec_name + ' ' + memberList[i].spec_level,
                    desc: 'Job: ' + memberList[i].job.capitalize()
                },
                data: {
                    loyalty: memberList[i].loyalty,
                    wage: memberList[i].wage,
                    job: memberList[i].job,
                    stats: memberList[i].stats,
                    spec_name: memberList[i].spec_name,
                    spec_level: memberList[i].spec_level,
                    skills: memberList[i].skills
                }
            };
        }

        // Now add the parent keys to the members

        Object.keys(members.chartMembers).forEach(function(k) {
            let member = members.chartMembers[k];
            if (k != '-1') { // Leader does not need a parent key
                member.parent = members.chartMembers[memberList[member.i].supervisor];
            }
            chart_config.push(member);
        });
        
        membersTree = new Treant(chart_config);
        //membersTree.tree.reload();

        if (recruit !== null) {
            let notification = getByClass('recruit-notification')[0];
            notification.style.display = 'block';
            getByQuery('.recruit-notification .recruiter-name').innerHTML = 
                members.chartMembers[recruit.supervisor].text.name;
            getByQuery('.recruit-notification .recruit-name').innerHTML = recruit.name;

            notification.addEventListener('click', function() {
                members.memberSelected = null;
                getByClass('details__none')[0].style.display = 'none';
                getByClass('details__info')[0].style.display = 'block';
                getByClass('details__jobs')[0].style.display = 'none';
                getByClass('details__learn')[0].style.display = 'none';
                getByClass('details__manage')[0].style.display = 'none';

                getByQuery('.details__info h1').innerHTML = recruit.name;
                getByQuery('.details__info h2').innerHTML = 
                    recruit.spec_name + ' ' + recruit.spec_level;
                getByQuery('.details__info .info__stats .int').innerHTML = recruit.stats[0];
                getByQuery('.details__info .info__stats .soc').innerHTML = recruit.stats[1];
                getByQuery('.details__info .info__stats .ste').innerHTML = recruit.stats[2];
                getByQuery('.details__info .info__stats .str').innerHTML = recruit.stats[3];
                getByQuery('.details__info .info__wage b').innerHTML = 
                    currency.format(recruit.wage);
                getByQuery('.details__info .info__loyalty b').innerHTML = recruit.loyalty;

                getByClass('accept-recruit')[0].style.display = 'inline-block';
                getByClass('reject-recruit')[0].style.display = 'inline-block';

                getByClass('accept-recruit')[0].addEventListener('click', function() {
                    alerty.confirm('Are you sure you want to accept this recruit?', {
                        title: 'Confirmation',
                        okLabel: 'Yes',
                        cancelLabel: 'No'
                    }, function() {
                        socket.send(JSON.stringify({
                            type: 'recruit',
                            choice: 'accept'
                        }));

                        notification.style.display = 'none';
                        getByClass('accept-recruit')[0].style.display = 'none';
                        getByClass('reject-recruit')[0].style.display = 'none';

                        alerty.toasts('Recruit accepted!', {
                            bgColor: '#35444e',
                            fontColor: '#fefefe',
                            time: 2500
                        });

                        deleteOverlays();
                    }, function() {
                        deleteOverlays();
                    });
                });
                getByClass('reject-recruit')[0].addEventListener('click', function() {
                    alerty.confirm('Are you sure you want to reject this recruit?', {
                        title: 'Confirmation',
                        okLabel: 'Yes',
                        cancelLabel: 'No'
                    }, function() {
                        socket.send(JSON.stringify({
                            type: 'recruit',
                            choice: 'reject'
                        }));

                        notification.style.display = 'none';
                        getByClass('accept-recruit')[0].style.display = 'none';
                        getByClass('reject-recruit')[0].style.display = 'none';

                        alerty.toasts('Recruit rejected!', {
                            bgColor: '#35444e',
                            fontColor: '#fefefe',
                            time: 2500
                        });

                        deleteOverlays();
                    }, function() {
                        deleteOverlays();
                    });
                });
            });
        }

        let chartNodes = document.querySelectorAll('.tabs__members .chart .node')
        for (let i = 0; i < chartNodes.length; i++) {
            if (chartNodes[i].classList.contains('-1')) {
                // No event listener for the leader ('You')
                continue;
            }
            chartNodes[i].addEventListener('click', members.selectMember);
        }
    },
    selectJob: function(e) {
        socket.send(JSON.stringify({
            type: 'job_change',
            cultist: members.chartMembers[members.memberSelected].HTMLclass,
            job: this.innerHTML.toLowerCase()
        }));

        members.chartMembers[members.memberSelected].data.job = this.innerHTML.toLowerCase();
        let node = getByClass( members.chartMembers[members.memberSelected].HTMLclass)[0];
        node.children[2].innerHTML = 'Job: ' + this.innerHTML;
        members.setTabData('jobs');
    },
    selectMember: function(e) {
        getByClass('details__none')[0].style.display = 'none';
        getByClass('details__info')[0].style.display = 'none';
        getByClass('details__jobs')[0].style.display = 'none';
        getByClass('details__learn')[0].style.display = 'none';
        getByClass('details__manage')[0].style.display = 'none';
        getByClass('accept-recruit')[0].style.display = 'none';
        getByClass('reject-recruit')[0].style.display = 'none';

        members.memberSelected = this.classList[1];
        
        members.setTabData('info');
    },
    selectTab: function(e) {
        if (members.memberSelected === null) return false;

        element = this;
        getByClass('details__none')[0].style.display = 'none';
        getByClass('details__info')[0].style.display = 'none';
        getByClass('details__jobs')[0].style.display = 'none';
        getByClass('details__learn')[0].style.display = 'none';
        getByClass('details__manage')[0].style.display = 'none';

        if (element.classList.contains('tabs__info'))
            members.setTabData('info');
        else if (element.classList.contains('tabs__jobs'))
            members.setTabData('jobs');
        else if (element.classList.contains('tabs__learn'))
            members.setTabData('learn');
        else if (element.classList.contains('tabs__manage'))
            members.setTabData('manage');
        else
            console.error('Unknown member details tab clicked!');
    },
    setTabData: function(tabName) {
        let member = members.chartMembers[members.memberSelected];
        if (tabName == 'info') {
            getByClass('details__info')[0].style.display = 'block';
            getByQuery('.details__info h1').innerHTML = member.text.name;
            getByQuery('.details__info h2').innerHTML = 
                member.data.spec_name + ' ' + member.data.spec_level;
            getByQuery('.details__info .info__stats .int').innerHTML = member.data.stats[0];
            getByQuery('.details__info .info__stats .soc').innerHTML = member.data.stats[1];
            getByQuery('.details__info .info__stats .ste').innerHTML = member.data.stats[2];
            getByQuery('.details__info .info__stats .str').innerHTML = member.data.stats[3];
            getByQuery('.details__info .info__wage b').innerHTML = 
                currency.format(member.data.wage);
            getByQuery('.details__info .info__loyalty b').innerHTML = member.data.loyalty;
        } else if (tabName == 'jobs') {
            // Add available jobs to dropdown menu
            let jobListEl = getByQuery('.job-list');
            jobListEl.innerHTML = '';
            let jobList = members.jobList;

            for (let i = 0; i < jobList.length; i++) {
                if (jobList[i] == member.data.job) {
                    // This is the cultist's current job
                    continue;
                }
                // Check if cultist qualifies for job
                if (jobList[i] == 'pickpocketing') {
                    if (member.data.spec_name != 'Pickpocketer') {
                        continue;
                    }
                }
                let job = document.createElement('div');
                job.innerHTML = jobList[i].capitalize();
                jobListEl.appendChild(job);
                job.addEventListener('click', members.selectJob);
            }

            getByClass('details__jobs')[0].style.display = 'block';
            let currentJob = getByQuery('.details__jobs h1');
            currentJob.innerHTML = 'Current job: ' + member.data.job.capitalize();
        } else if (tabName == 'learn') {
            getByClass('details__learn')[0].style.display = 'block';
        } else if (tabName == 'manage') {
            getByClass('details__manage')[0].style.display = 'block';
        } else {
            console.error('Unknown member tab name.');
        }
    },
    promoteMember: function(e) {
        alerty.alert('This feature is not complete yet.', {
            title: 'Oops!',
            okLabel: 'OK'
        });
    },
    kickMember: function(e) {
        alerty.confirm('Are you sure you want to kick ' + 
            members.chartMembers[members.memberSelected].text.name + 
            ' out of the cult? This action is not reversable!', {
            title: 'Confirmation',
            okLabel: 'Yes',
            cancelLabel: 'No'
        }, function() {
            socket.send(JSON.Stringify({
                type: 'manage_recruit',
                command: 'kick',
                id: members.chartMembers[members.memberSelected].HTMLclass
            }));
            
            alerty.toasts('Cultist kicked out!', {
                bgColor: '#35444e',
                fontColor: '#fefefe',
                time: 2500
            });

            deleteOverlays();
        }, function () {
            deleteOverlays();
        });
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

                deleteOverlays();
            }, function() {
                deleteOverlays();
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
                });

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

                deleteOverlays();
            }, function() {
                deleteOverlays();
            });
        }
    },
    setData: function(upgrade) { // Fill in the detail text spots
        getByQuery('.headquarters__details h2').innerHTML = upgrade.name;
        getByQuery('.stats__data .cost').innerHTML = currency.format(upgrade.cost);
        getByQuery('.stats__text').innerHTML = '<p>' + upgrade.description + '</p>';
    },
    upgrades: {
        windowbars: {
            name: 'Window Security Bars',
            id: 'windowbars',
            cost: 2500,
            'description': 'Prevent intruders from entering through the windows - unless they have a metal cutter.'
        },
        motionsensors: {
            name: 'Motion Sensors',
            id: 'motionsensors',
            cost: 5000,
            description: 'Detect movement in unauthorized areas. Keep in mind that experienced thieves have methods for getting past them.'
        },
        cctv: {
            name: 'CCTV System',
            id: 'cctv',
            cost: 7500,
            description: 'Set up security cameras around the area. You will need guards to monitor the cameras, though.'
        },
        ups: {
            name: 'Uninterruptible Power Supply',
            id: 'ups',
            cost: 10000,
            description: 'An emergency power supply in case the power goes out for any reason.'
        },
        insurance: {
            name: 'Insurance',
            id: 'insurance',
            cost: 25000,
            description: 'In case of a successful burglary, you get back 10% of money lost.'
        },
        doorsystem: {
            name: 'Door Access Control System',
            id: 'doorsystem',
            cost: 75000,
            description: 'All employees are given keycards that are used to open doors. Even though it makes a lockpicker useless, a technician could bypass it easily.'
        },
        jammers: {
            name: 'Signal Jammers',
            id: 'jammers',
            cost: 100000,
            description: 'Block any incoming signals to protect against hackers.'
        },
        fencing: {
            name: 'Perimeter Fencing',
            id: 'fencing',
            cost: 125000,
            description: 'Barbed wire metal fences that circle the perimeter to prevent unauthorized property access.'
        },
        lockdownsystem: {
            name: 'Emergency Lockdown System',
            id: 'lockdownsystem',
            cost: 150000,
            description: 'In case of a detected intrusion, block all doors and windows from opening.'
        }
    },
};

let currency = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
}),
    connected = false,
    visible = true,
    animationFinished = true,
    tabSwitchFinished = true,
    firstMembersVisit = true,
    firstHQVisit = true,
    active = 'home',
    socket;

window.addEventListener('load', function() { // Once page loaded and parsed
    contacts.setActiveContact('anonymous');

    getByClass('menu__tabs')[0].addEventListener('click', chat.setActiveMenuTab);
    getByClass('menu__chat')[0].addEventListener('click', chat.setActiveMenuTab);

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
        if (document.contains(getByClass('spinner')[0])) {
            getByClass('spinner')[0].remove();
        }
        connected = true; // Allow tab switching etc.

        // Set 'home' as the initial tab
        setActiveTab({target: getById('tabs-list__home')}, false);

        let tabs = document.querySelectorAll('.tabs-list li');
        for (let i = 0; i < tabs.length; i++) {
            tabs[i].addEventListener('click', setActiveTab);
        }
    };

    socket.onclose = function(code) {
        console.debug('WebSocket connection closed.');
        console.log(code);
    };

    socket.onerror = function(err) {
        // console.error(err);
    };

    socket.onmessage = function(message) { // The consumer sends us a message
        let data = JSON.parse(message.data);
        if (data.type == 'page_data') {
            setPage(data); // We are sent data about a requested page
        } else if (data.type == 'page_redirect') { // Server wants to change the active tab
            console.log(data.page);
            setActiveTab({target: getById('tabs-list__' + data.page)});
        } else if (data.type == 'multiple_connections') {
            console.log('WebSocket connection closed due to another connection.');
            socket.close();
            socket = undefined;
            alerty.alert('Your account has connected to the game from somewhere \
            else. Make sure you don\'t have the game open in another tab.', {
                title: 'Connection closed',
                okLabel: 'OK'
            });
        } else if (data.type == 'tutorial_lock') {
            alerty.alert('You are not permitted to do this kind of action during the tutorial!', {
                title: 'Tutorial Lock',
                okLabel: 'OK'
            });
        }
    };

    getById('create-cult__form').addEventListener('submit', function(e) {
        e.preventDefault(); // Don't submit the form, instead send it over websockets
        socket.send(JSON.stringify({
            type: 'create_cult',
            cult_data: {
                cult_name: getById('cult-name').value,
                cult_type: getByQuery('input[name="cult-type"]:checked').value
            }
        }));
    });

    getByClass('nav__logout')[0].addEventListener('click', function() {
        alerty.confirm('Are you sure you want to log out?', {
            title: 'Confirmation',
            okLabel: 'Yes',
            cancelLabel: 'No'
        }, function() {
            window.location.replace('../logout');
            deleteOverlays();
        }, function() {
            deleteOverlays();
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

    window.onerror = function(msg, url, linenumber) {
        alert('Error message: '+msg+'\nURL: '+url+'\nLine Number: '+linenumber);
        return true;
    }

    new VanillaKinetic(getByClass('chart')[0], {
        cursor: '',
        slowdown: 0.1
    });

    // Double-clicking on the edges will make the chart move
    // Should be used if dragging doesn't work for some reason
    getByClass('chart')[0].addEventListener('click', function(e) {
        if (e.target.tagName == 'svg') { // Don't detect clicks on nodes
            let rect = this.getBoundingClientRect();
            let offsetX = e.clientX - rect.left;
            let offsetY = e.clientY - rect.top;
            if (offsetY <= 50) {
                this.scrollBy(0, -100);
            } else if (this.offsetHeight - 50 <= offsetY) {
                this.scrollBy(0, 100);
            } else if (offsetX <= 50) {
                this.scrollBy(-100, 0);
            } else if (this.offsetWidth - 50 <= offsetX) {
                this.scrollBy(100, 0);
            } 
        }
    }, false);

    window.onresize = function() {
        if (!visible) {
            let tabs = getByQuery('.sidebar--visible');
            tabs.style.marginLeft = '-' + (tabs.offsetWidth + 1) + 'px';
        }

        if (getByClass('menu__chat')[0].classList.contains('active')) {
            let screenHeight = document.documentElement.clientHeight;
            let otherHeight = getByQuery('nav').offsetHeight + 40 +
                getByQuery('.menu__list').offsetHeight +
                getByQuery('.chat__input').offsetHeight;

            getByClass('chat__text')[0].style.height = 
                (screenHeight - otherHeight) + 'px';
        }
    };
});

// I realise that this whole file is a huge mess
// I'll rewrite it sooner or later (by that I mean never)
