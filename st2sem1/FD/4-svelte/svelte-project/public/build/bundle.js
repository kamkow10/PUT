
(function(l, r) { if (l.getElementById('livereloadscript')) return; r = l.createElement('script'); r.async = 1; r.src = '//' + (window.location.host || 'localhost').split(':')[0] + ':35729/livereload.js?snipver=1'; r.id = 'livereloadscript'; l.getElementsByTagName('head')[0].appendChild(r) })(window.document);
var app = (function () {
    'use strict';

    function noop() { }
    function add_location(element, file, line, column, char) {
        element.__svelte_meta = {
            loc: { file, line, column, char }
        };
    }
    function run(fn) {
        return fn();
    }
    function blank_object() {
        return Object.create(null);
    }
    function run_all(fns) {
        fns.forEach(run);
    }
    function is_function(thing) {
        return typeof thing === 'function';
    }
    function safe_not_equal(a, b) {
        return a != a ? b == b : a !== b || ((a && typeof a === 'object') || typeof a === 'function');
    }
    function is_empty(obj) {
        return Object.keys(obj).length === 0;
    }

    function append(target, node) {
        target.appendChild(node);
    }
    function insert(target, node, anchor) {
        target.insertBefore(node, anchor || null);
    }
    function detach(node) {
        node.parentNode.removeChild(node);
    }
    function destroy_each(iterations, detaching) {
        for (let i = 0; i < iterations.length; i += 1) {
            if (iterations[i])
                iterations[i].d(detaching);
        }
    }
    function element(name) {
        return document.createElement(name);
    }
    function text(data) {
        return document.createTextNode(data);
    }
    function space() {
        return text(' ');
    }
    function listen(node, event, handler, options) {
        node.addEventListener(event, handler, options);
        return () => node.removeEventListener(event, handler, options);
    }
    function attr(node, attribute, value) {
        if (value == null)
            node.removeAttribute(attribute);
        else if (node.getAttribute(attribute) !== value)
            node.setAttribute(attribute, value);
    }
    function children(element) {
        return Array.from(element.childNodes);
    }
    function set_input_value(input, value) {
        input.value = value == null ? '' : value;
    }
    function custom_event(type, detail) {
        const e = document.createEvent('CustomEvent');
        e.initCustomEvent(type, false, false, detail);
        return e;
    }

    let current_component;
    function set_current_component(component) {
        current_component = component;
    }

    const dirty_components = [];
    const binding_callbacks = [];
    const render_callbacks = [];
    const flush_callbacks = [];
    const resolved_promise = Promise.resolve();
    let update_scheduled = false;
    function schedule_update() {
        if (!update_scheduled) {
            update_scheduled = true;
            resolved_promise.then(flush);
        }
    }
    function add_render_callback(fn) {
        render_callbacks.push(fn);
    }
    let flushing = false;
    const seen_callbacks = new Set();
    function flush() {
        if (flushing)
            return;
        flushing = true;
        do {
            // first, call beforeUpdate functions
            // and update components
            for (let i = 0; i < dirty_components.length; i += 1) {
                const component = dirty_components[i];
                set_current_component(component);
                update(component.$$);
            }
            set_current_component(null);
            dirty_components.length = 0;
            while (binding_callbacks.length)
                binding_callbacks.pop()();
            // then, once components are updated, call
            // afterUpdate functions. This may cause
            // subsequent updates...
            for (let i = 0; i < render_callbacks.length; i += 1) {
                const callback = render_callbacks[i];
                if (!seen_callbacks.has(callback)) {
                    // ...so guard against infinite loops
                    seen_callbacks.add(callback);
                    callback();
                }
            }
            render_callbacks.length = 0;
        } while (dirty_components.length);
        while (flush_callbacks.length) {
            flush_callbacks.pop()();
        }
        update_scheduled = false;
        flushing = false;
        seen_callbacks.clear();
    }
    function update($$) {
        if ($$.fragment !== null) {
            $$.update();
            run_all($$.before_update);
            const dirty = $$.dirty;
            $$.dirty = [-1];
            $$.fragment && $$.fragment.p($$.ctx, dirty);
            $$.after_update.forEach(add_render_callback);
        }
    }
    const outroing = new Set();
    function transition_in(block, local) {
        if (block && block.i) {
            outroing.delete(block);
            block.i(local);
        }
    }
    function mount_component(component, target, anchor, customElement) {
        const { fragment, on_mount, on_destroy, after_update } = component.$$;
        fragment && fragment.m(target, anchor);
        if (!customElement) {
            // onMount happens before the initial afterUpdate
            add_render_callback(() => {
                const new_on_destroy = on_mount.map(run).filter(is_function);
                if (on_destroy) {
                    on_destroy.push(...new_on_destroy);
                }
                else {
                    // Edge case - component was destroyed immediately,
                    // most likely as a result of a binding initialising
                    run_all(new_on_destroy);
                }
                component.$$.on_mount = [];
            });
        }
        after_update.forEach(add_render_callback);
    }
    function destroy_component(component, detaching) {
        const $$ = component.$$;
        if ($$.fragment !== null) {
            run_all($$.on_destroy);
            $$.fragment && $$.fragment.d(detaching);
            // TODO null out other refs, including component.$$ (but need to
            // preserve final state?)
            $$.on_destroy = $$.fragment = null;
            $$.ctx = [];
        }
    }
    function make_dirty(component, i) {
        if (component.$$.dirty[0] === -1) {
            dirty_components.push(component);
            schedule_update();
            component.$$.dirty.fill(0);
        }
        component.$$.dirty[(i / 31) | 0] |= (1 << (i % 31));
    }
    function init(component, options, instance, create_fragment, not_equal, props, dirty = [-1]) {
        const parent_component = current_component;
        set_current_component(component);
        const $$ = component.$$ = {
            fragment: null,
            ctx: null,
            // state
            props,
            update: noop,
            not_equal,
            bound: blank_object(),
            // lifecycle
            on_mount: [],
            on_destroy: [],
            on_disconnect: [],
            before_update: [],
            after_update: [],
            context: new Map(parent_component ? parent_component.$$.context : options.context || []),
            // everything else
            callbacks: blank_object(),
            dirty,
            skip_bound: false
        };
        let ready = false;
        $$.ctx = instance
            ? instance(component, options.props || {}, (i, ret, ...rest) => {
                const value = rest.length ? rest[0] : ret;
                if ($$.ctx && not_equal($$.ctx[i], $$.ctx[i] = value)) {
                    if (!$$.skip_bound && $$.bound[i])
                        $$.bound[i](value);
                    if (ready)
                        make_dirty(component, i);
                }
                return ret;
            })
            : [];
        $$.update();
        ready = true;
        run_all($$.before_update);
        // `false` as a special case of no DOM component
        $$.fragment = create_fragment ? create_fragment($$.ctx) : false;
        if (options.target) {
            if (options.hydrate) {
                const nodes = children(options.target);
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                $$.fragment && $$.fragment.l(nodes);
                nodes.forEach(detach);
            }
            else {
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                $$.fragment && $$.fragment.c();
            }
            if (options.intro)
                transition_in(component.$$.fragment);
            mount_component(component, options.target, options.anchor, options.customElement);
            flush();
        }
        set_current_component(parent_component);
    }
    /**
     * Base class for Svelte components. Used when dev=false.
     */
    class SvelteComponent {
        $destroy() {
            destroy_component(this, 1);
            this.$destroy = noop;
        }
        $on(type, callback) {
            const callbacks = (this.$$.callbacks[type] || (this.$$.callbacks[type] = []));
            callbacks.push(callback);
            return () => {
                const index = callbacks.indexOf(callback);
                if (index !== -1)
                    callbacks.splice(index, 1);
            };
        }
        $set($$props) {
            if (this.$$set && !is_empty($$props)) {
                this.$$.skip_bound = true;
                this.$$set($$props);
                this.$$.skip_bound = false;
            }
        }
    }

    function dispatch_dev(type, detail) {
        document.dispatchEvent(custom_event(type, Object.assign({ version: '3.38.2' }, detail)));
    }
    function append_dev(target, node) {
        dispatch_dev('SvelteDOMInsert', { target, node });
        append(target, node);
    }
    function insert_dev(target, node, anchor) {
        dispatch_dev('SvelteDOMInsert', { target, node, anchor });
        insert(target, node, anchor);
    }
    function detach_dev(node) {
        dispatch_dev('SvelteDOMRemove', { node });
        detach(node);
    }
    function listen_dev(node, event, handler, options, has_prevent_default, has_stop_propagation) {
        const modifiers = options === true ? ['capture'] : options ? Array.from(Object.keys(options)) : [];
        if (has_prevent_default)
            modifiers.push('preventDefault');
        if (has_stop_propagation)
            modifiers.push('stopPropagation');
        dispatch_dev('SvelteDOMAddEventListener', { node, event, handler, modifiers });
        const dispose = listen(node, event, handler, options);
        return () => {
            dispatch_dev('SvelteDOMRemoveEventListener', { node, event, handler, modifiers });
            dispose();
        };
    }
    function attr_dev(node, attribute, value) {
        attr(node, attribute, value);
        if (value == null)
            dispatch_dev('SvelteDOMRemoveAttribute', { node, attribute });
        else
            dispatch_dev('SvelteDOMSetAttribute', { node, attribute, value });
    }
    function prop_dev(node, property, value) {
        node[property] = value;
        dispatch_dev('SvelteDOMSetProperty', { node, property, value });
    }
    function set_data_dev(text, data) {
        data = '' + data;
        if (text.wholeText === data)
            return;
        dispatch_dev('SvelteDOMSetData', { node: text, data });
        text.data = data;
    }
    function validate_each_argument(arg) {
        if (typeof arg !== 'string' && !(arg && typeof arg === 'object' && 'length' in arg)) {
            let msg = '{#each} only iterates over array-like objects.';
            if (typeof Symbol === 'function' && arg && Symbol.iterator in arg) {
                msg += ' You can use a spread to convert this iterable into an array.';
            }
            throw new Error(msg);
        }
    }
    function validate_slots(name, slot, keys) {
        for (const slot_key of Object.keys(slot)) {
            if (!~keys.indexOf(slot_key)) {
                console.warn(`<${name}> received an unexpected slot "${slot_key}".`);
            }
        }
    }
    /**
     * Base class for Svelte components with some minor dev-enhancements. Used when dev=true.
     */
    class SvelteComponentDev extends SvelteComponent {
        constructor(options) {
            if (!options || (!options.target && !options.$$inline)) {
                throw new Error("'target' is a required option");
            }
            super();
        }
        $destroy() {
            super.$destroy();
            this.$destroy = () => {
                console.warn('Component was already destroyed'); // eslint-disable-line no-console
            };
        }
        $capture_state() { }
        $inject_state() { }
    }

    /* src\App.svelte generated by Svelte v3.38.2 */

    const file = "src\\App.svelte";

    function get_each_context(ctx, list, i) {
    	const child_ctx = ctx.slice();
    	child_ctx[19] = list[i];
    	return child_ctx;
    }

    // (110:16) {#each todosToShow as todo}
    function create_each_block(ctx) {
    	let div;
    	let label;
    	let input;
    	let input_checked_value;
    	let t0;
    	let t1_value = /*todo*/ ctx[19].text + "";
    	let t1;
    	let t2;
    	let button;
    	let t4;
    	let mounted;
    	let dispose;

    	function click_handler() {
    		return /*click_handler*/ ctx[15](/*todo*/ ctx[19]);
    	}

    	function click_handler_1() {
    		return /*click_handler_1*/ ctx[16](/*todo*/ ctx[19]);
    	}

    	const block = {
    		c: function create() {
    			div = element("div");
    			label = element("label");
    			input = element("input");
    			t0 = space();
    			t1 = text(t1_value);
    			t2 = space();
    			button = element("button");
    			button.textContent = "Usuń";
    			t4 = space();
    			attr_dev(input, "type", "checkbox");
    			input.checked = input_checked_value = /*todo*/ ctx[19].done;
    			add_location(input, file, 112, 28, 3185);
    			add_location(label, file, 111, 24, 3149);
    			attr_dev(button, "class", "btn btn-secondary btn-lg svelte-qoxuxi");
    			attr_dev(button, "type", "button");
    			add_location(button, file, 115, 24, 3362);
    			attr_dev(div, "class", "checkbox svelte-qoxuxi");
    			add_location(div, file, 110, 20, 3102);
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, div, anchor);
    			append_dev(div, label);
    			append_dev(label, input);
    			append_dev(label, t0);
    			append_dev(label, t1);
    			append_dev(div, t2);
    			append_dev(div, button);
    			append_dev(div, t4);

    			if (!mounted) {
    				dispose = [
    					listen_dev(input, "click", click_handler, false, false, false),
    					listen_dev(button, "click", click_handler_1, false, false, false)
    				];

    				mounted = true;
    			}
    		},
    		p: function update(new_ctx, dirty) {
    			ctx = new_ctx;

    			if (dirty & /*todosToShow*/ 4 && input_checked_value !== (input_checked_value = /*todo*/ ctx[19].done)) {
    				prop_dev(input, "checked", input_checked_value);
    			}

    			if (dirty & /*todosToShow*/ 4 && t1_value !== (t1_value = /*todo*/ ctx[19].text + "")) set_data_dev(t1, t1_value);
    		},
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(div);
    			mounted = false;
    			run_all(dispose);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_each_block.name,
    		type: "each",
    		source: "(110:16) {#each todosToShow as todo}",
    		ctx
    	});

    	return block;
    }

    function create_fragment(ctx) {
    	let main;
    	let div7;
    	let div0;
    	let h1;
    	let t0;
    	let span;
    	let t1_value = /*todos*/ ctx[1].length + "";
    	let t1;
    	let t2;
    	let div1;
    	let label0;
    	let input0;
    	let t3;
    	let t4;
    	let label1;
    	let input1;
    	let t5;
    	let t6;
    	let label2;
    	let input2;
    	let t7;
    	let t8;
    	let div3;
    	let div2;
    	let t9;
    	let div6;
    	let div5;
    	let div4;
    	let input3;
    	let t10;
    	let button;
    	let mounted;
    	let dispose;
    	let each_value = /*todosToShow*/ ctx[2];
    	validate_each_argument(each_value);
    	let each_blocks = [];

    	for (let i = 0; i < each_value.length; i += 1) {
    		each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
    	}

    	const block = {
    		c: function create() {
    			main = element("main");
    			div7 = element("div");
    			div0 = element("div");
    			h1 = element("h1");
    			t0 = text("nodeTODO: ");
    			span = element("span");
    			t1 = text(t1_value);
    			t2 = space();
    			div1 = element("div");
    			label0 = element("label");
    			input0 = element("input");
    			t3 = text("\n                ALL");
    			t4 = space();
    			label1 = element("label");
    			input1 = element("input");
    			t5 = text("\n                TODO");
    			t6 = space();
    			label2 = element("label");
    			input2 = element("input");
    			t7 = text("\n                DONE");
    			t8 = space();
    			div3 = element("div");
    			div2 = element("div");

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				each_blocks[i].c();
    			}

    			t9 = space();
    			div6 = element("div");
    			div5 = element("div");
    			div4 = element("div");
    			input3 = element("input");
    			t10 = space();
    			button = element("button");
    			button.textContent = "Dodaj";
    			attr_dev(span, "class", "label label-info");
    			add_location(span, file, 89, 26, 2319);
    			add_location(h1, file, 89, 12, 2305);
    			attr_dev(div0, "class", "jumbotron text-center");
    			add_location(div0, file, 88, 8, 2257);
    			attr_dev(input0, "type", "radio");
    			input0.__value = "ALL";
    			input0.value = input0.__value;
    			/*$$binding_groups*/ ctx[9][0].push(input0);
    			add_location(input0, file, 94, 16, 2470);
    			attr_dev(label0, "class", "svelte-qoxuxi");
    			add_location(label0, file, 93, 12, 2446);
    			attr_dev(input1, "type", "radio");
    			input1.__value = "TODO";
    			input1.value = input1.__value;
    			/*$$binding_groups*/ ctx[9][0].push(input1);
    			add_location(input1, file, 98, 16, 2634);
    			attr_dev(label1, "class", "svelte-qoxuxi");
    			add_location(label1, file, 97, 12, 2610);
    			attr_dev(input2, "type", "radio");
    			input2.__value = "DONE";
    			input2.value = input2.__value;
    			/*$$binding_groups*/ ctx[9][0].push(input2);
    			add_location(input2, file, 102, 16, 2800);
    			attr_dev(label2, "class", "svelte-qoxuxi");
    			add_location(label2, file, 101, 12, 2776);
    			attr_dev(div1, "id", "radios");
    			attr_dev(div1, "class", "radios svelte-qoxuxi");
    			add_location(div1, file, 92, 8, 2401);
    			attr_dev(div2, "class", "col-sm-8 col-sm-offset-2");
    			add_location(div2, file, 108, 12, 2999);
    			attr_dev(div3, "id", "todo-list");
    			attr_dev(div3, "class", "row svelte-qoxuxi");
    			add_location(div3, file, 107, 8, 2954);
    			attr_dev(input3, "id", "newTodo");
    			attr_dev(input3, "type", "text");
    			attr_dev(input3, "class", "form-control input-lg text-center");
    			attr_dev(input3, "placeholder", "co jeszcze chcesz zrobić?");
    			add_location(input3, file, 126, 20, 3746);
    			attr_dev(div4, "class", "form-group");
    			add_location(div4, file, 125, 16, 3701);
    			attr_dev(button, "class", "btn btn-primary btn-lg");
    			add_location(button, file, 129, 16, 3945);
    			attr_dev(div5, "class", "col-sm-8 col-sm-offset-2 text-center");
    			add_location(div5, file, 124, 12, 3634);
    			attr_dev(div6, "id", "todo-form");
    			attr_dev(div6, "class", "row svelte-qoxuxi");
    			add_location(div6, file, 123, 8, 3589);
    			attr_dev(div7, "class", "container");
    			add_location(div7, file, 86, 4, 2224);
    			add_location(main, file, 84, 0, 2212);
    		},
    		l: function claim(nodes) {
    			throw new Error("options.hydrate only works if the component was compiled with the `hydratable: true` option");
    		},
    		m: function mount(target, anchor) {
    			insert_dev(target, main, anchor);
    			append_dev(main, div7);
    			append_dev(div7, div0);
    			append_dev(div0, h1);
    			append_dev(h1, t0);
    			append_dev(h1, span);
    			append_dev(span, t1);
    			append_dev(div7, t2);
    			append_dev(div7, div1);
    			append_dev(div1, label0);
    			append_dev(label0, input0);
    			input0.checked = input0.__value === /*showOption*/ ctx[3];
    			append_dev(label0, t3);
    			append_dev(div1, t4);
    			append_dev(div1, label1);
    			append_dev(label1, input1);
    			input1.checked = input1.__value === /*showOption*/ ctx[3];
    			append_dev(label1, t5);
    			append_dev(div1, t6);
    			append_dev(div1, label2);
    			append_dev(label2, input2);
    			input2.checked = input2.__value === /*showOption*/ ctx[3];
    			append_dev(label2, t7);
    			append_dev(div7, t8);
    			append_dev(div7, div3);
    			append_dev(div3, div2);

    			for (let i = 0; i < each_blocks.length; i += 1) {
    				each_blocks[i].m(div2, null);
    			}

    			append_dev(div7, t9);
    			append_dev(div7, div6);
    			append_dev(div6, div5);
    			append_dev(div5, div4);
    			append_dev(div4, input3);
    			set_input_value(input3, /*text*/ ctx[0]);
    			append_dev(div5, t10);
    			append_dev(div5, button);

    			if (!mounted) {
    				dispose = [
    					listen_dev(input0, "change", /*input0_change_handler*/ ctx[8]),
    					listen_dev(input0, "change", /*change_handler*/ ctx[10], false, false, false),
    					listen_dev(input1, "change", /*input1_change_handler*/ ctx[11]),
    					listen_dev(input1, "change", /*change_handler_1*/ ctx[12], false, false, false),
    					listen_dev(input2, "change", /*input2_change_handler*/ ctx[13]),
    					listen_dev(input2, "change", /*change_handler_2*/ ctx[14], false, false, false),
    					listen_dev(input3, "input", /*input3_input_handler*/ ctx[17]),
    					listen_dev(button, "click", /*click_handler_2*/ ctx[18], false, false, false)
    				];

    				mounted = true;
    			}
    		},
    		p: function update(ctx, [dirty]) {
    			if (dirty & /*todos*/ 2 && t1_value !== (t1_value = /*todos*/ ctx[1].length + "")) set_data_dev(t1, t1_value);

    			if (dirty & /*showOption*/ 8) {
    				input0.checked = input0.__value === /*showOption*/ ctx[3];
    			}

    			if (dirty & /*showOption*/ 8) {
    				input1.checked = input1.__value === /*showOption*/ ctx[3];
    			}

    			if (dirty & /*showOption*/ 8) {
    				input2.checked = input2.__value === /*showOption*/ ctx[3];
    			}

    			if (dirty & /*deleteTodo, todosToShow, updateTodo*/ 52) {
    				each_value = /*todosToShow*/ ctx[2];
    				validate_each_argument(each_value);
    				let i;

    				for (i = 0; i < each_value.length; i += 1) {
    					const child_ctx = get_each_context(ctx, each_value, i);

    					if (each_blocks[i]) {
    						each_blocks[i].p(child_ctx, dirty);
    					} else {
    						each_blocks[i] = create_each_block(child_ctx);
    						each_blocks[i].c();
    						each_blocks[i].m(div2, null);
    					}
    				}

    				for (; i < each_blocks.length; i += 1) {
    					each_blocks[i].d(1);
    				}

    				each_blocks.length = each_value.length;
    			}

    			if (dirty & /*text*/ 1 && input3.value !== /*text*/ ctx[0]) {
    				set_input_value(input3, /*text*/ ctx[0]);
    			}
    		},
    		i: noop,
    		o: noop,
    		d: function destroy(detaching) {
    			if (detaching) detach_dev(main);
    			/*$$binding_groups*/ ctx[9][0].splice(/*$$binding_groups*/ ctx[9][0].indexOf(input0), 1);
    			/*$$binding_groups*/ ctx[9][0].splice(/*$$binding_groups*/ ctx[9][0].indexOf(input1), 1);
    			/*$$binding_groups*/ ctx[9][0].splice(/*$$binding_groups*/ ctx[9][0].indexOf(input2), 1);
    			destroy_each(each_blocks, detaching);
    			mounted = false;
    			run_all(dispose);
    		}
    	};

    	dispatch_dev("SvelteRegisterBlock", {
    		block,
    		id: create_fragment.name,
    		type: "component",
    		source: "",
    		ctx
    	});

    	return block;
    }

    function instance($$self, $$props, $$invalidate) {
    	let { $$slots: slots = {}, $$scope } = $$props;
    	validate_slots("App", slots, []);
    	let text = "";
    	let todos = [];
    	let todosToShow = [];
    	let showOption = "ALL";

    	fetch("http://localhost:4000/api/todos").then(response => response.json()).then(data => {
    		$$invalidate(1, todos = data);
    		showTodos();
    	});

    	function updateTodo(todo) {
    		todo.done = !todo.done;

    		const requestOptions = {
    			method: "PATCH",
    			headers: { "Content-Type": "application/json" },
    			body: JSON.stringify(todo)
    		};

    		fetch("http://localhost:4000/api/todos", requestOptions).then(response => response.json()).then(data => {
    			$$invalidate(1, todos = data);
    			showTodos();
    		});
    	}

    	function deleteTodo(id) {
    		const requestOptions = { method: "DELETE" };

    		fetch("http://localhost:4000/api/todos/" + id, requestOptions).then(response => response.json()).then(data => {
    			$$invalidate(1, todos = data);
    			showTodos();
    		});
    	}

    	function createTodo() {
    		const requestOptions = {
    			method: "POST",
    			headers: { "Content-Type": "application/json" },
    			body: JSON.stringify({ text })
    		};

    		fetch("http://localhost:4000/api/todos/", requestOptions).then(response => response.json()).then(data => {
    			$$invalidate(1, todos = data);
    			showTodos();
    			$$invalidate(0, text = "");
    		});
    	}

    	function showTodos() {
    		if (todos.length === 0) {
    			$$invalidate(2, todosToShow = []);
    			return;
    		}

    		for (let todo of todos) {
    			switch (showOption) {
    				case "DONE":
    					$$invalidate(2, todosToShow = todos.filter(todo => {
    						return todo.done;
    					}));
    					break;
    				case "TODO":
    					$$invalidate(2, todosToShow = todos.filter(todo => {
    						return !todo.done;
    					}));
    					break;
    				case "ALL":
    					$$invalidate(2, todosToShow = todos);
    					break;
    			}
    		}
    	}

    	const writable_props = [];

    	Object.keys($$props).forEach(key => {
    		if (!~writable_props.indexOf(key) && key.slice(0, 2) !== "$$") console.warn(`<App> was created with unknown prop '${key}'`);
    	});

    	const $$binding_groups = [[]];

    	function input0_change_handler() {
    		showOption = this.__value;
    		$$invalidate(3, showOption);
    	}

    	const change_handler = () => showTodos();

    	function input1_change_handler() {
    		showOption = this.__value;
    		$$invalidate(3, showOption);
    	}

    	const change_handler_1 = () => showTodos();

    	function input2_change_handler() {
    		showOption = this.__value;
    		$$invalidate(3, showOption);
    	}

    	const change_handler_2 = () => showTodos();
    	const click_handler = todo => updateTodo(todo);
    	const click_handler_1 = todo => deleteTodo(todo._id);

    	function input3_input_handler() {
    		text = this.value;
    		$$invalidate(0, text);
    	}

    	const click_handler_2 = () => createTodo();

    	$$self.$capture_state = () => ({
    		text,
    		todos,
    		todosToShow,
    		showOption,
    		updateTodo,
    		deleteTodo,
    		createTodo,
    		showTodos
    	});

    	$$self.$inject_state = $$props => {
    		if ("text" in $$props) $$invalidate(0, text = $$props.text);
    		if ("todos" in $$props) $$invalidate(1, todos = $$props.todos);
    		if ("todosToShow" in $$props) $$invalidate(2, todosToShow = $$props.todosToShow);
    		if ("showOption" in $$props) $$invalidate(3, showOption = $$props.showOption);
    	};

    	if ($$props && "$$inject" in $$props) {
    		$$self.$inject_state($$props.$$inject);
    	}

    	return [
    		text,
    		todos,
    		todosToShow,
    		showOption,
    		updateTodo,
    		deleteTodo,
    		createTodo,
    		showTodos,
    		input0_change_handler,
    		$$binding_groups,
    		change_handler,
    		input1_change_handler,
    		change_handler_1,
    		input2_change_handler,
    		change_handler_2,
    		click_handler,
    		click_handler_1,
    		input3_input_handler,
    		click_handler_2
    	];
    }

    class App extends SvelteComponentDev {
    	constructor(options) {
    		super(options);
    		init(this, options, instance, create_fragment, safe_not_equal, {});

    		dispatch_dev("SvelteRegisterComponent", {
    			component: this,
    			tagName: "App",
    			options,
    			id: create_fragment.name
    		});
    	}
    }

    const app = new App({
    	target: document.body,
    	props: {
    		name: 'world'
    	}
    });

    return app;

}());
//# sourceMappingURL=bundle.js.map
