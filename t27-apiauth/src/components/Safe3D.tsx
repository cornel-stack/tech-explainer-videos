import React from "react";

// If the three.js canvas throws (e.g. no WebGL context on a CI runner), render
// the 2D fallback instead of failing the whole frame/shard.
export class Safe3D extends React.Component<
  { fallback: React.ReactNode; children: React.ReactNode },
  { failed: boolean }
> {
  state = { failed: false };
  static getDerivedStateFromError() {
    return { failed: true };
  }
  componentDidCatch(err: unknown) {
    // eslint-disable-next-line no-console
    console.warn("Safe3D: 3D hero failed, using 2D fallback —", err);
  }
  render() {
    return this.state.failed ? this.props.fallback : this.props.children;
  }
}
