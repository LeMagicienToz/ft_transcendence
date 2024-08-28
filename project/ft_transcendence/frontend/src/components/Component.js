export class Component {
    constructor(props = {}) {
        this.props = props;
        this.state = {};
        this.container = null;
    }

    // Called when the component is first rendered
    componentDidMount() {}

    // Called just before the component is removed from the DOM
    componentWillUnmount() {}

    // Set the state and re-render the component
    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.renderComponent();
    }

    // To be overridden by the specific component
    render() {
        return '';
    }

    // Called to render the component in the DOM
    renderComponent() {
        if (this.container) {
            this.container.innerHTML = this.render();
            this.addEventListeners();
        }
    }

    // To be overridden if the component has event listeners
    addEventListeners() {}

    // Initial render
    mount(container) {
        this.container = container;
        this.renderComponent();
        this.componentDidMount();
    }

    // Unmount the component and call lifecycle hook
    unmount() {
        this.componentWillUnmount();
        if (this.container) {
            this.container.innerHTML = '';
        }
    }
}