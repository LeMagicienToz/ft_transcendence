export class Store {
    constructor(initialState = {}) {
        this.state = initialState;
        this.listeners = [];
    }

    getState() {
        return this.state;
    }

    subscribe(listener) {
        this.listeners.push(listener);
    }

    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.notify();
    }

    notify() {
        this.listeners.forEach(listener => listener(this.state));
    }
}

/*
// Example usage:
const appStore = new Store({ count: 0, user: { name: 'John Doe' } });

// Subscribe a component to the store
appStore.subscribe((state) => {
    console.log('State updated:', state);
});
*/