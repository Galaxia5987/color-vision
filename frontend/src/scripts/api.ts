const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? '').replace(/\/+$/, '')

const apiUrl = (path: string) => {
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path
  }
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE_URL}${normalizedPath}`
}

export class ApiError extends Error {
  status: number
  body: unknown

  constructor(status: number, message: string, body: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.body = body
  }
}

const requestJson = async <T>(path: string, options: RequestInit = {}): Promise<T> => {
  const headers = new Headers(options.headers)
  if (!headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  const response = await fetch(apiUrl(path), {
    ...options,
    headers,
  })

  if (!response.ok) {
    let body: unknown = null
    try {
      body = await response.json()
    } catch {
      body = await response.text()
    }
    throw new ApiError(response.status, response.statusText, body)
  }

  return (await response.json()) as T
}

const requestText = async (path: string, options: RequestInit = {}): Promise<string> => {
  const response = await fetch(apiUrl(path), options)
  if (!response.ok) {
    let body: unknown = null
    try {
      body = await response.json()
    } catch {
      body = await response.text()
    }
    throw new ApiError(response.status, response.statusText, body)
  }
  return response.text()
}

export type Detection = {
  limits: [number[], number[]]
  min_area: number
  max_area: number
}

export type CameraConfig = {
  name: string
  detection_stream_enabled: boolean
  mask_stream_enabled: boolean
  detection: Detection
  exposure: number
}

export type RootConfig = {
  cameras: CameraConfig[]
}

export type ListCamerasResponse = {
  cameras: CameraConfig[]
}

export type UpdateCameraSettingsResponse = {
  camera: CameraConfig
  runner_active: boolean
}

export type SaveConfigResponse = {
  status: string
  path: string
}

export type ReloadConfigResponse = {
  status: string
  config: RootConfig
}

export const getConfig = () => requestJson<RootConfig>('/api/config')

export const listCameras = () => requestJson<ListCamerasResponse>('/api/cameras')

export const updateCameraSettings = (cameraName: string, update: CameraConfig) =>
  requestJson<UpdateCameraSettingsResponse>(`/api/cameras/${encodeURIComponent(cameraName)}`, {
    method: 'PATCH',
    body: JSON.stringify(update),
  })

export const saveConfig = (config?: RootConfig | null) =>
  requestJson<SaveConfigResponse>('/api/config/save', {
    method: 'POST',
    body: JSON.stringify(config ?? null),
  })

export const reloadConfig = () =>
  requestJson<ReloadConfigResponse>('/api/config/reload', { method: 'POST' })

export const getStreamsHome = () => requestText('/streams/')

export const getStreamUrl = (cameraName: string, streamName: string) =>
  apiUrl(`/streams/${encodeURIComponent(cameraName)}/${encodeURIComponent(streamName)}`)

export const listDevices = () =>
  requestJson<Array<string>>("/api/available_cameras")

export const addCamera = (cameraName: string) =>
  requestText(`/api/cameras/add/${cameraName}`, {method: 'PUT'})
