export type ToastType = "success" | "error" | "info" | "warning";

export interface Toast {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

let toastId = 0;
const listeners: ((toast: Toast) => void)[] = [];

export function useToast() {
  const show = (message: string, type: ToastType = "info", duration = 3000) => {
    const id = String(++toastId);
    const toast: Toast = { id, type, message, duration };
    listeners.forEach((listener) => listener(toast));

    if (duration) {
      setTimeout(() => {
        dismiss(id);
      }, duration);
    }

    return id;
  };

  const dismiss = (id: string) => {
    // This would be handled by the Toast provider
  };

  return {
    success: (message: string) => show(message, "success"),
    error: (message: string) => show(message, "error"),
    info: (message: string) => show(message, "info"),
    warning: (message: string) => show(message, "warning"),
    dismiss,
  };
}

export function subscribe(listener: (toast: Toast) => void) {
  listeners.push(listener);
  return () => {
    const index = listeners.indexOf(listener);
    if (index > -1) {
      listeners.splice(index, 1);
    }
  };
}
