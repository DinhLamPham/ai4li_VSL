/**
 * API Service - Tất cả API calls đến backend
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_V1_PREFIX = '/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL + API_V1_PREFIX,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 300000, // 5 minutes
})

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('[API Error]', error.response?.data || error.message)
    throw error
  }
)

// VSL Recognition API
export const vslRecognitionAPI = {
  /**
   * Nhận diện VSL từ video
   * @param {File} videoFile - Video file
   * @returns {Promise}
   */
  recognizeVideo: async (videoFile) => {
    const formData = new FormData()
    formData.append('file', videoFile)

    return apiClient.post('/vsl/recognize-video', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  /**
   * Nhận diện VSL từ image
   * @param {File} imageFile - Image file
   * @returns {Promise}
   */
  recognizeImage: async (imageFile) => {
    const formData = new FormData()
    formData.append('file', imageFile)

    return apiClient.post('/vsl/recognize-image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  /**
   * Lấy danh sách gestures
   * @returns {Promise}
   */
  getGestures: async () => {
    return apiClient.get('/vsl/gestures')
  },

  /**
   * Detect gesture từ file
   * @param {File} file - Image or video file
   * @returns {Promise}
   */
  detectGesture: async (file) => {
    const formData = new FormData()
    formData.append('file', file)

    return apiClient.post('/vsl/gesture/detect', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  /**
   * Detect emotion từ image
   * @param {File} imageFile - Image file
   * @returns {Promise}
   */
  detectEmotion: async (imageFile) => {
    const formData = new FormData()
    formData.append('file', imageFile)

    return apiClient.post('/vsl/emotion/detect', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// Speech Processing API
export const speechAPI = {
  /**
   * Chuyển audio thành text (STT)
   * @param {File} audioFile - Audio file
   * @returns {Promise}
   */
  audioToText: async (audioFile) => {
    const formData = new FormData()
    formData.append('file', audioFile)

    return apiClient.post('/speech/audio-to-text', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  /**
   * Chuyển text thành audio (TTS)
   * @param {string} text - Text to convert
   * @param {object} options - TTS options
   * @returns {Promise}
   */
  textToAudio: async (text, options = {}) => {
    return apiClient.post('/speech/text-to-audio', {
      text,
      voice: options.voice || null,
      language: options.language || 'vi',
    })
  },

  /**
   * Lấy danh sách voices
   * @returns {Promise}
   */
  getVoices: async () => {
    return apiClient.get('/speech/voices')
  },
}

// Text to VSL API
export const textToVSLAPI = {
  /**
   * Chuyển text thành VSL gloss
   * @param {string} text - Vietnamese text
   * @param {object} options - Translation options
   * @returns {Promise}
   */
  textToVSL: async (text, options = {}) => {
    return apiClient.post('/vsl/text-to-vsl', {
      text,
      options,
    })
  },

  /**
   * Generate 3D avatar animation
   * @param {string} text - Vietnamese text
   * @param {object} options - Animation options
   * @returns {Promise}
   */
  generateAvatar: async (text, options = {}) => {
    return apiClient.post('/vsl/generate-avatar', {
      text,
      options,
    })
  },

  /**
   * Lấy VSL vocabulary
   * @returns {Promise}
   */
  getVocabulary: async () => {
    return apiClient.get('/vsl/vocabulary')
  },

  /**
   * Create gloss annotation
   * @param {string} videoPath - Video path
   * @param {string} gloss - VSL gloss
   * @returns {Promise}
   */
  createAnnotation: async (videoPath, gloss) => {
    return apiClient.post('/vsl/gloss-tool/annotate', null, {
      params: { video_path: videoPath, gloss },
    })
  },
}

// Data & Tools API
export const toolsAPI = {
  /**
   * Augment data file
   * @param {File} file - Data file
   * @param {string[]} augmentationTypes - Types of augmentation
   * @returns {Promise}
   */
  augmentData: async (file, augmentationTypes) => {
    const formData = new FormData()
    formData.append('file', file)

    return apiClient.post('/tools/augment', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      params: { augmentation_types: augmentationTypes },
    })
  },

  /**
   * Validate dataset
   * @param {string} dataDir - Dataset directory
   * @param {string} dataType - Data type
   * @returns {Promise}
   */
  validateDataset: async (dataDir, dataType) => {
    return apiClient.get('/tools/dataset/validate', {
      params: { data_dir: dataDir, data_type: dataType },
    })
  },

  /**
   * Generate dataset report
   * @param {string} dataDir - Dataset directory
   * @returns {Promise}
   */
  getDatasetReport: async (dataDir) => {
    return apiClient.get('/tools/dataset/report', {
      params: { data_dir: dataDir },
    })
  },

  /**
   * List all models
   * @param {string} modelType - Model type filter
   * @returns {Promise}
   */
  listModels: async (modelType = null) => {
    return apiClient.get('/tools/models/list', {
      params: modelType ? { model_type: modelType } : {},
    })
  },

  /**
   * Upload model
   * @param {File} modelFile - Model file
   * @param {object} metadata - Model metadata
   * @returns {Promise}
   */
  uploadModel: async (modelFile, metadata) => {
    const formData = new FormData()
    formData.append('file', modelFile)

    return apiClient.post('/tools/models/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      params: metadata,
    })
  },

  /**
   * Benchmark model
   * @param {string} modelPath - Model path
   * @param {string} testDataDir - Test data directory
   * @returns {Promise}
   */
  benchmarkModel: async (modelPath, testDataDir) => {
    return apiClient.post('/tools/models/benchmark', null, {
      params: { model_path: modelPath, test_data_dir: testDataDir },
    })
  },
}

export default apiClient
