export type CameraStatus = 'online' | 'offline'

export type CameraOption = {
  id: string
  displayName: string
  status: CameraStatus
}

export type StreamDefinition = {
  id: string
  title: string
  description: string
}

export type ProcessingMode = {
  label: string
  value: string
}

export type StreamViewOption = {
  label: string
  value: string
}

export type DangerAction = {
  id: string
  label: string
  description: string
}

export const cameraOptions: CameraOption[] = [
  {
    id: 'color-01',
    displayName: 'color-01',
    status: 'online',
  },
  {
    id: 'color-02',
    displayName: 'color-02',
    status: 'offline',
  }
]

export const streamDefinitions: StreamDefinition[] = [
  {
    id: 'raw',
    title: 'Raw Feed',
    description: 'Before processing',
  },
  {
    id: 'processed',
    title: 'Target Feed',
    description: 'After vision pipeline',
  }
]

export const streamViewOptions: StreamViewOption[] = [
  { label: 'Overlay', value: 'overlay' },
  { label: 'Heatmap', value: 'heatmap' },
  { label: 'Contours', value: 'contours' }
]

export const resolutionOptions: ProcessingMode[] = [
  { label: '1920 x 1080', value: '1080p' },
  { label: '1280 x 720', value: '720p' },
  { label: '960 x 540', value: '540p' }
]

export const processingModes: ProcessingMode[] = [
  { label: 'Color Detection Pipeline', value: 'color' }
]

export const dangerActions: DangerAction[] = [
  {
    id: 'restart',
    label: 'Restart Service',
    description: 'Reboot the vision service and reconnect.'
  }
]

export const statusSeverityMap: Record<CameraStatus, 'success' | 'warning' | 'danger'> = {
  online: 'success',
  offline: 'danger'
}
