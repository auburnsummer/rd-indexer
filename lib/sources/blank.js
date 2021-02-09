// A driver is a standardised set of functions which implement getting levels from a source.
// implement these to add support for a service.

/* eslint-disable */
module.exports = class {
	// The driver constructor can take any arbitary number of arguments as required. The arguments are
	// given via the YAML. However...
	constructor({}) {
		// ...the constructor must set this property:

		// If true, Orchard will rehost the rdzips on Backblaze and use that for the download link.
		// NOTE: Orchard will _always_ rehost the rdzips regardless. This just decides if the DL link is IPFS or not.
		this.rehost = false;
	}

	// A function which is called when the driver is loaded. Any initialisation should occur here.
	async init() {

	}

	// Return an array of iids. This is some value which has both these properties:
	//  - An iid maps to exactly one level;
	//  - If the level changes, the iid also changes.
	// for instance, you can't edit a level in Discord without reuploading it, so the URL can be the IID.
	// however, you can edit Steam Workshop levels, so for Workshop the IID needs to be a combination of
	// the last updated date and the level ID.
	async getIids() {

	}

	// Given an IID, return the download URL. If rehost is true, this function is not called.
	async getDownloadLink(iid) {

	}

	// Given a driver-specific object, 

	// Given an IID, return the rdzip that maps to that IID as an arraybuffer (i.e. download the level)
	async get(iid) {

	}

	// A function which gets called after the driver is done, including on errors.
	async cleanup() {

	}

};

/* eslint-enable */
