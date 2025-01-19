import { createApp, h } from 'vue'

interface ToastOptions {
  message: string
  type?: 'success' | 'error' | 'warning' | 'info'
  duration?: number
}

const createToast = (options: ToastOptions) => {
  const { message, type = 'info', duration = 3000 } = options

  // 创建容器
  const container = document.createElement('div')
  container.className = 'fixed top-4 right-4 z-50 flex flex-col gap-2'
  document.body.appendChild(container)

  // 创建 toast 组件
  const ToastComponent = {
    props: ['message', 'type'],
    setup(props: ToastOptions) {
      const baseClasses = 'px-4 py-2 rounded-lg shadow-lg text-white transform transition-all duration-300'
      const typeClasses = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-yellow-500',
        info: 'bg-blue-500'
      }

      return () => h(
        'div',
        {
          class: `${baseClasses} ${typeClasses[props.type || 'info']}`
        },
        props.message
      )
    }
  }

  // 挂载 toast
  const toastApp = createApp(ToastComponent, {
    message,
    type
  })

  const toastElement = document.createElement('div')
  container.appendChild(toastElement)
  toastApp.mount(toastElement)

  // 自动移除
  setTimeout(() => {
    toastApp.unmount()
    toastElement.remove()
    if (container.childNodes.length === 0) {
      container.remove()
    }
  }, duration)
}

export const toast = {
  success(message: string) {
    createToast({ message, type: 'success' })
  },
  error(message: string) {
    createToast({ message, type: 'error' })
  },
  warning(message: string) {
    createToast({ message, type: 'warning' })
  },
  info(message: string) {
    createToast({ message, type: 'info' })
  }
} 