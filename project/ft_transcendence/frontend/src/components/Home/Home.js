import { Component } from "../Component";
import { Counter } from "../Counter/Counter";

export class Home extends Component {
    render() {
        return `
            <section class="p-3">
                <h2>Home Page</h2>
                <p>Welcome to the home page.</p>
                <div id="counter"></div>
            </section>
        `;
    }

    componentDidMount() {
        const counter = new Counter({ store: this.props.store });
        counter.mount(document.getElementById('counter'));
    }
}