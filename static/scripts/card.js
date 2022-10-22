const body = document.getElementsByTagName('html');

//Add your document event listener
document.addEventListener('click', async (e) => {
    //Get the event listener target
    const target = e?.target || window?.event?.target || e?.srcElement;

    //Make sure the target is valid
    if (!target) {
        console.error('Target cannot be null!');
        return;
    }

    //Handle the GLASS nodes (?)
    if (target.nodeName === 'GLASS') {
        body[0].removeChild(body[0].firstChild);
        return;
    }

    //Fetch the card's data
    const card = target.parentElement.nodeName === 'CARD' ? target.parentElement : target;
    const links = card.lastElementChild.children;
    const name =  card.childNodes[3].innerText;

    //Print out the card's data
    console.log('Current target data', {
        card,
        links,
        name,
        target
    });

    //Fetch the data from anilist
    const resp = await anilist(name);

    //Check to make sure anilist returned data
    if(!resp) return; 

    //Handle the data if it was returned
    handleData(resp, links);
}, false);

//This function handles fetching data from a specific URL
async function getData(url, options) {
    //setup something for us to store the error data
    let err;
    try {
        //Use the browser fetch API to get the response
        let response = await fetch(url, options);
        //If the response was ok, return the deserialized data
        if (response.ok) return response.json();

        //Response wasn't ok, we need to return the response data
        err = response;
    } catch (error) {
        //An exception was thrown by `fetch`, pass the error on to the error handler
        err = error; 
    }

    //Log out the error information
    console.error('An error occurred while fetching resource', {
        url,
        options,
        err
    });
    //Alert the user that something went wrong
    alert(`Whoups we probably don't have any info about this anime!`);

    //return dumby data for us to use later
    return null;
}

//Short hand function for dealing with graphQL queries
function graphql(url, query, variables) {
    return getData(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            query,
            variables
        })
    })
}

//Short hand function for fetching anilist anime data
function anilist(name) {
    const QUERY = `
query ($name: String) { 
    # Define which variables will be used in the query (id)
    Media (search: $name, type: ANIME) { 
        # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
        idMal
        description
        bannerImage
        coverImage {
            extraLarge
        }
        tags {
            name
        }
        title {
            romaji
            english
            native
        }
    }
}`;
    return graphql('https://graphql.anilist.co', QUERY, { name });
}

//This is your handle data function just copy and pasted
function handleData(data, links) {
    console.log(data);
    const glass = document.createElement("glass")
    const card_big = document.createElement("card-big")
    card_big.style.backgroundImage = `url(${data.data.Media.bannerImage})`
    const card_big_title = document.createElement("div")

    const card_big_title__eng = document.createElement("p")
    const card_big_title__jp = document.createElement("p")

    card_big_title__eng.textContent = data.data.Media.title.english
    card_big_title__jp.textContent = data.data.Media.title.native

    card_big_title__eng.setAttribute('class', "card_big_title--en")
    card_big_title__jp.setAttribute('class', "card_big_title--jp")

    card_big_title.setAttribute('class', "card_big_title")

    const card_big_img = document.createElement("div")

    card_big_img.style.backgroundImage = `url(${data.data.Media.coverImage.extraLarge})`
    card_big_img.setAttribute('class', "card_big_img")
    
    const card_big_links = document.createElement("div")
    card_big_links.setAttribute('class', "card_big_links")

    const card_big_link = document.createElement("a")
    card_big_link.setAttribute('class', "card_big_link")
    card_big_link.setAttribute('href', `https://myanimelist.net/anime/${data.data.Media.idMal})`)

    

    const card_big_link_img = document.createElement("img")
    card_big_link_img.setAttribute("src", "static\\img\\MAL-icon.png")
    card_big_link.appendChild(card_big_link_img)
    
    card_big_links.appendChild(card_big_link)


    for(var i = 0; i < (links.length - 1); i++)
    {
        const card_big_link = document.createElement("a")
        card_big_link.setAttribute('class', "card_big_link")
        card_big_link.setAttribute('href', links[i].firstElementChild.href)

        const card_big_link_img = document.createElement("img")
        if (links[i].firstElementChild.host == "funimation.com")
        {
            card_big_link_img.setAttribute("src", "static\\img\\funimation-icon.png")
        }
        else if (links[i].firstElementChild.host == "crunchyroll.com")
        {
            card_big_link_img.setAttribute("src", "static\\img\\crunchyroll-icon.png")
        }
        else if (links[i].firstElementChild.host == "hidive.com")
        {
            card_big_link_img.setAttribute("src", "static\\img\\hidive-icon.png")
        }
        else if (links[i].firstElementChild.host == "animego.org")
        {
            card_big_link_img.setAttribute("src", "static\\img\\animego-icon.png")
        }
        else
        {
            card_big_link_img.setAttribute("src", "static\\img\\loading.gif")
        }
        card_big_link.appendChild(card_big_link_img)
    
        card_big_links.appendChild(card_big_link)
    }


    const card_big_tags = document.createElement("div")
    card_big_tags.setAttribute('class', "card_big_tags")
    
    const card_big_tag_1 = document.createElement("div")
    card_big_tag_1.setAttribute('class', "card_big_tag")
    card_big_tag_1.textContent = data.data.Media.tags[0].name
    card_big_tags.appendChild(card_big_tag_1)

    const card_big_tag_2 = document.createElement("div")
    card_big_tag_2.setAttribute('class', "card_big_tag")
    card_big_tag_2.textContent = data.data.Media.tags[1].name
    card_big_tags.appendChild(card_big_tag_2)

    const card_big_tag_3 = document.createElement("div")
    card_big_tag_3.setAttribute('class', "card_big_tag")
    card_big_tag_3.textContent = data.data.Media.tags[2].name
    card_big_tags.appendChild(card_big_tag_3)

    const card_big_tag_4 = document.createElement("div")
    card_big_tag_4.setAttribute('class', "card_big_tag")
    card_big_tag_4.textContent = data.data.Media.tags[3].name
    card_big_tags.appendChild(card_big_tag_4)

    const card_big_tag_5 = document.createElement("div")
    card_big_tag_5.setAttribute('class', "card_big_tag")
    card_big_tag_5.textContent = data.data.Media.tags[4].name
    card_big_tags.appendChild(card_big_tag_5)

    const card_big_desc = document.createElement("div")
    card_big_desc.setAttribute('class', "card_big_desc")

    card_big_desc.innerHTML = data.data.Media.description


    card_big_title.appendChild(card_big_title__eng)
    card_big_title.appendChild(card_big_title__jp)

    card_big.appendChild(card_big_title)
    card_big.appendChild(card_big_img)
    card_big.appendChild(card_big_tags)
    card_big.appendChild(card_big_links)
    card_big.appendChild(card_big_desc)
    
    glass.appendChild(card_big)

    body[0].insertBefore(glass, body[0].firstChild)
}