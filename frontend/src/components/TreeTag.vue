<template>
  <div>
    {{tagTreeTitle}}
    <Tree
      id="my-tree-id"
      ref="my-tree"
      :custom-options="myCustomOptions"
      :custom-styles="myCustomStyles"
      :nodes="treeDisplayData"
    ></Tree>
    <b-modal 
        ref="edit-modal" 
        ok-only 
        no-close-on-esc 
        no-close-on-backdrop
        @ok="handleOk"
      >
      <div class="withMargin">
        <b-form-input v-model="newName" placeholder="New name"></b-form-input>
      </div>
    </b-modal>
  </div>
</template>

<script>
import Tree from "vuejs-tree";

export default {
  name: "TreeExample",
  components: {
    Tree,
  },
  props: ['tagTreeTitle', 'treeDisplayData'],
  data: function () {
    return {
      editNodeId: undefined,
      newName: ""
    };
  },
  computed: {
    myCustomStyles() {
      return {
        tree: {
          height: "auto",
          maxHeight: "300px",
          overflowY: "visible",
          display: "inline-block",
          textAlign: "left",
        },
        row: {
          style: {
            width: "500px",
            cursor: "pointer",
          },
          child: {
            class: "",
            style: {
              height: "35px",
            },
            active: {
              style: {
                height: "35px",
              },
            },
          },
        },
        rowIndent: {
          paddingLeft: "20px",
        },
        text: {
          // class: "" // uncomment this line to overwrite the 'capitalize' class, or add a custom class
          style: {},
          active: {
            style: {
              "font-weight": "bold",
              color: "#2ECC71",
            },
          },
        },
      };
    },
    myCustomOptions() {
      return {
        treeEvents: {
          expanded: {
            state: false,
          },
          collapsed: {
            state: false,
          },
          selected: {
            state: false,
            fn: this.mySelectedFunction,
          },
          checked: {
            state: true,
            fn: this.myCheckedFunction,
          },
        },
        events: {
          expanded: {
            state: true,
          },
          selected: {
            state: false,
          },
          checked: {
            state: true,
          },
          editableName: {
            state: true,
            calledEvent: "expanded",
          },
        },
        addNode: {
          state: true,
          fn: this.addNodeFunction,
          appearOnHover: false,
        },
        editNode: { 
          state: true, 
          fn: this.editNodeFunction, 
          appearOnHover: false 
        },
        deleteNode: {
          state: true,
          fn: this.deleteNodeFunction,
          appearOnHover: true,
        },
        showTags: true,
      };
    },
  },
  // mounted() {
  //   this.$refs["my-tree"].expandNode(1);
  // },
  methods: {
    myCheckedFunction: function (nodeId, state) {
      console.log(this.treeDisplayData)
      console.log(`is ${nodeId} checked ? ${state}`); 
      //sendevents
    },
    // mySelectedFunction: function (nodeId, state) {
    //   console.log(`is ${nodeId} selected ? ${state}`);
    //   console.log(this.$refs["my-tree"].getSelectedNode());
    //   const node = this.$refs["my-tree"].findNode(5);
    //   const newState = node.state;
    //   newState.checked = state;
    //   this.$set(node, "state", newState);
    //   console.log(this.$refs["my-tree"].findNode(5).state);
    // },
    deleteNodeFunction: function (node) {
      this.$emit('delete-node', node.id)
    },
    editNodeFunction: function (node) {
      this.editNodeId = node.id;
      this.$refs['edit-modal'].show()
    },
    handleOk: function() {
      this.$emit('edit-node', this.editNodeId, this.newName)
    },
    addNodeFunction: function (node) {
      if (node.nodes === undefined) {
        // the node doesn't have childs
        // I use $set to ensure that VueJs detect the change
        console.log('Disabled parent node creation')
        // this.$set(node, "nodes", [newNode]);
      } else {
        this.$emit('create-node', node.id)
      }
    },
  },
};
</script>

<style scoped>
</style>