import apiConfig from "@src/config/apiConfig";
import axios from "axios";

const ApiService = axios.create({
	baseURL: apiConfig.apiUrl || 'http://localhost:8000'
})

export default ApiService
