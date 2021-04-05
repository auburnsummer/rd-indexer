const { default: axios } = require("axios");
const delay = require("delay");

const { some, endsWith, flatten } = require("lodash");
const DL = require("../../download");

const BASE_URL = "https://discord.com/api"

const URL = "https://auburnsummer.github.io"
const VERSION_NUMBER = "0.0.1"

module.exports = class {
	constructor({botToken, channelID, after}) {
        this.botToken = botToken;
        this.channelID = channelID;
        this.after = BigInt(after);
        this.before = false;

        // ...the constructor must set this property:

		// If true, Orchard will rehost the rdzips on Backblaze and use that for the download link.
		// NOTE: Orchard will _always_ rehost the rdzips regardless. This just decides if the DL link is BB or not.
		this.rehost = false;
	}

	// A function which is called when the driver is loaded. Any initialisation should occur here.
	async init() {
        this.results = [];
        let escape = false;
        while (!escape) {
            const {data, headers} = await axios({
                url: `${BASE_URL}/channels/${this.channelID}/messages`,
                validateStatus: () => true,
                method: "GET",
                headers: {
                    Authorization: `Bot ${this.botToken}`,
                    "User-Agent": `DiscordBot (${URL}, ${VERSION_NUMBER})`
                },
                params: {
                    // don't include before the first time.
                    ...this.before ? {before: this.before} : {},
                    limit: 100
                }
            });
            if (data.retry_after) {
                console.log(`we're being rate limited, waiting ${data.retry_after} sec...`)
                await delay(data.retry_after * 1000);
                continue;
            }
            for (let r of data) {
                // discord IDs are in order, so any ID after the previous one 
                const snowflake = BigInt(r.id);
                if (snowflake <= this.after) {
                    escape = true;
                    break;
                } else {
                    this.results.push(r);
                    this.before = r.id;
                }
            }
            // calculate how long to wait.
            const waitTime= parseInt(headers['x-ratelimit-reset-after']) / (parseInt(headers['x-ratelimit-remaining']) + 1)
            console.log(`Waiting ${waitTime} seconds...`)
            await delay(waitTime * 1000);
            
        }
        this.iids = flatten(this.results.map(message => {
            return message.attachments.filter(a => endsWith(a.url, ".rdzip")).map(a => a.url);
        }));
	}

	// Return an array of iids. This is some value which has both these properties:
	//  - An iid maps to exactly one level;
	//  - If the level changes, the iid also changes.
	// for instance, you can't edit a level in Discord without reuploading it, so the URL can be the IID.
	// however, you can edit Steam Workshop levels, so for Workshop the IID needs to be a combination of
	// the last updated date and the level ID.
	async getIids() {
        return this.iids;
	}

	// Given an IID, return the download URL. If rehost is true, this function is not called.
	async getDownloadLink(iid) {
        return iid;
	}

	// Given a driver-specific object, 

	// Given an IID, return the rdzip that maps to that IID as an arraybuffer (i.e. download the level)
	async get(iid) {
        const resp = await DL(iid);
		return resp.data;
	}

	// A function which gets called after the driver is done, including on errors.
	async cleanup() {
        
	}

};

/* eslint-enable */
