const API_URL = "https://script.google.com/macros/s/AKfycbzm3I9ENulE7uOmze53cyDuj7Igi7fmGiQ6w045fCRxs_sK3D4/exec";

const {default: axios} = require('axios');
const { flatten } = require('lodash');

(async () => {
    // get data...
    const data = await axios({
        method: "GET",
        url: API_URL
    })
        .then( (resp) => {
            return resp.data;
        });
    
    const payload = data
        // if verified doesn't exist, we haven't bothered with it b4
        .filter(level => level.verified != null)
        .map(level => {
            if (level.verified) {
                return [
                    {
                        "op": "add",
                        "path": "/-",
                        "value": {
                            "action": "approval",
                            "set": 10,
                            "s_id": "rdl",
                            "s_iid": level.download_url
                        }
                    },
                    {
                        "op": "add",
                        "path": "/-",
                        "value": {
                            "action": "approval",
                            "set": 10,
                            "s_id": "yeoldesheet",
                            "s_iid": level.download_url
                        }
                    },
                ]
            } else {
                return [
                    {
                        "op": "add",
                        "path": "/-",
                        "value": {
                            "action": "approval",
                            "set": -1,
                            "s_id": "rdl",
                            "s_iid": level.download_url
                        }
                    },
                    {
                        "op": "add",
                        "path": "/-",
                        "value": {
                            "action": "approval",
                            "set": -1,
                            "s_id": "yeoldesheet",
                            "s_iid": level.download_url
                        }
                    },
                ]
            }
        });

    const payload2 = flatten(payload);
  
    await axios({
        method: "PATCH",
        data: payload2,
        url: process.env.LODGE_URL,
        headers: {
            authorization: `Token ${process.env.LODGE_TOKEN}`
        }
    })

    console.log("done")


})();