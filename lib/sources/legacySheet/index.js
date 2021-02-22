const axios = require("axios");

const {map, get, slice} = require("lodash/fp");

const _ = require("lodash");
const DL = require("../../download");

const frozen = require("./freeze_2021-02-20.json");

const API_URL = "https://script.google.com/macros/s/AKfycbzm3I9ENulE7uOmze53cyDuj7Igi7fmGiQ6w045fCRxs_sK3D4/exec";

module.exports = class {
	constructor() {
		this.rehost = false;
	}

	async init() {
		this.data = frozen;
        // this.data = await axios({
        //     method: "GET",
        //     url: API_URL
        // })
        //     .then( (resp) => {
        //         return resp.data;
        //     })
	}

	async getIids() {
		const iids = map(get("download_url"), this.data);
		return iids;
	}

	async getDownloadLink(iid) {
        return iid;
	}

	async get(iid) {
        const resp = await DL(iid);
		return resp.data;
	}

	async onChangeHook() {

	}

	async cleanup() {

	}

};

/* eslint-enable */
