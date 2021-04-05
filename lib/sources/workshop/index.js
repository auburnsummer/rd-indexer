// A driver is a standardised set of functions which implement getting levels from a source.
// implement these to add support for a service.
const axios = require("axios");
const DL = require("../../download");

const rdID = "774181";

/* eslint-disable */
module.exports = class {
	// The driver constructor can take any arbitary number of arguments as required. The arguments are
	// given via the YAML. However...
	constructor({bluebell}) {
		// ...the constructor must set this property:

		// If true, Orchard will rehost the rdzips on Backblaze and use that for the download link.
		// NOTE: Orchard will _always_ rehost the rdzips regardless. This just decides if the DL link is BB or not.
		this.rehost = true;
		this.bluebell = bluebell;
	}

	// A function which is called when the driver is loaded. Any initialisation should occur here.
	async init() {
        this.data = await axios({
            method: "GET",
            url: `${this.bluebell}/${rdID}/levels`
        })
            .then( (resp) => {
                return resp.data;
            })
	}

	// Return an array of iids. This is some value which has both these properties:
	//  - An iid maps to exactly one level;
	//  - If the level changes, the iid also changes.
	// for instance, you can't edit a level in Discord without reuploading it, so the URL can be the IID.
	// however, you can edit Steam Workshop levels, so for Workshop the IID needs to be a combination of
	// the last updated date and the level ID.
	async getIids() {
		return this.data.map(r => r.iid);
	}

	// Given an IID, return the download URL. If rehost is true, this function is not called.
	async getDownloadLink(iid) {
		
	}

	// Given an IID, return the rdzip that maps to that IID as an arraybuffer (i.e. download the level)
	async get(iid) {
		const id = this.data.find(r => r.iid === iid).id;
        const resp = await DL(`${this.bluebell}/${rdID}/${id}`);
		return resp.data;
	}

	// A function which gets called after the driver is done, including on errors.
	async cleanup() {
		return axios({
			method: "GET",
			url: `${this.bluebell}/purge`
		})
	}	

};

/* eslint-enable */
