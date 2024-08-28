import { Component } from "../Component";

export class Counter extends Component {
    constructor(props) {
        super(props);
        this.state = {
            count: this.props.store.getState().count
        };
    }

    render() {
        return `
            <div>
                <h2>Count: ${this.state.count}</h2>
                <button id="increment" class="btn btn-primary">Increment</button>
                <button id="decrement" class="btn btn-secondary">Decrement</button>
            </div>
        `;
    }

    addEventListeners() {
        document.getElementById('increment').addEventListener('click', () => {
            this.props.store.setState({ count: this.state.count + 1 });
        });

        document.getElementById('decrement').addEventListener('click', () => {
            this.props.store.setState({ count: this.state.count - 1 });
        });
    }

    componentDidMount() {
        this.props.store.subscribe((state) => {
            if (this.state.count !== state.count) {
                this.setState({ count: state.count });
            }
        });
    }
}