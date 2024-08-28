import { Component } from "../Component";

export class Header extends Component {
    render() {
        return `
            <header class="bg-primary text-white p-3">
                <h1>${this.props.title}</h1>
                <nav>
                    <a href="/" data-link class="text-white">Home</a>
                    <a href="/about" data-link class="text-white ml-3">About</a>
                </nav>
            </header>
        `;
    }

    componentDidMount() {
        console.log('Header component mounted');
    }

    componentWillUnmount() {
        console.log('Header component will unmount');
    }
}