const API_URL = "https://script.google.com/macros/s/AKfycbzm3I9ENulE7uOmze53cyDuj7Igi7fmGiQ6w045fCRxs_sK3D4/exec";
const BOT_API_URL = "https://bot2.auburn.dev"

const TOKEN = "SXQT97gWnUDv3CtlLYqUHgVA7NBqpGYjwKj3U8WIrwAc97EMKoU4B6JBCUvcETGWi1XHxkBC6W4PvRUomjtAcme89OWK9Qsc0/7YETRhTEDQ7YhY7XvLcUArMg==";

const {default: axios} = require('axios');
const { flatten, isArray } = require('lodash');

(async () => {
    // get data...
    const data = await axios({
        method: "GET",
        url: API_URL
    })
        .then( (resp) => {
            return resp.data;
        });
    
    const approvedLevels = data.filter(r => r.verified);
    for (let level of approvedLevels) {
        console.log(level.download_url);
        const aaaa = await axios({
            method: "GET",
            url: "https://api.rhythm.cafe/orchard/level.json",
            params: {
                "_sort": "id",
                "url__exact": level.download_url,
                "_shape": "array"
            }
        });
        if (isArray(aaaa.data) && aaaa.data.length > 0) {
            // const resp = aaaa.data[0];
            // console.log(`Found a match, the id is ${resp.id}`);
            // if (resp.approval < 10) {
            //     const bbbb = await axios({
            //         method: 'POST',
            //         url: `${BOT_API_URL}/approval/${resp.id}`,
            //         data: {
            //             approval: 10
            //         },
            //         headers: {
            //             'authorization': `Bearer ${TOKEN}`
            //         }
            //     });
            //     console.log(bbbb.data);
            // } else {
            //     console.log("already > 10, ignoring...");
            // }
        }

    }
    console.log(data.length);
    console.log(approvedLevels.length);


})();