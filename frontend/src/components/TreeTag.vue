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
        hide-footer
        @ok="handleNewOk"
      >
      <div class="withMargin">
        <b-input-group>
          <b-form-input v-model="newName" placeholder="New name"></b-form-input>

          <b-input-group-append>
            <b-button v-if="edit" @click="handleEditOk">Edit</b-button>
            <b-button v-else @click="handleNewOk">Create</b-button>
          </b-input-group-append>
        </b-input-group>
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
      newName: "",
      edit: true
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
              height: "20px",
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
          style: {
            "font-size": "20px"
          },
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
  //   this.$refs["my-tree"].expandNode("Persone");
  // },
  watch: {
    treeDisplayData: function() {

    }
  },
  methods: {
    myCheckedFunction: function (nodeId, state) {
      console.log('this.treeDisplayData', this.treeDisplayData)
      console.log(`is ${nodeId} checked ? ${state}`); 
      const node = this.$refs["my-tree"].findNode(nodeId);
      if (node.nodes === undefined) {
        // the node doesn't have childs
        // I use $set to ensure that VueJs detect the change
        console.log('It is a child')
        // this.$set(node, "nodes", [newNode]);
      } else {
        for (let index in node.nodes) {
          node.nodes[index].state.checked = state
        }
      }
      // The following two lines seem to be necessary to update checked
      // state of children in case parent node changes state
      // const checkednode = this.$refs["my-tree"].findNode(nodeId);
      // this.$set(checkednode, state.checked, state);
      this.$emit('checked-node')
    },
    deleteNodeFunction: function (node) {
      this.$emit('delete-node', node.id)
    },
    editNodeFunction: function (node) {
      this.editNodeId = node.id;
      this.edit = true
      this.$refs['edit-modal'].show()
    },
    handleEditOk: function() {
      this.$emit('edit-node', this.editNodeId, this.newName)
      this.$refs['edit-modal'].hide()
    },
    handleNewOk: function() {
      this.$emit('create-node', this.editNodeId, this.newName)
      this.$refs['edit-modal'].hide()
    },
    addNodeFunction: function (node) {
      if (node.nodes === undefined) {
        // the node doesn't have childs
        // I use $set to ensure that VueJs detect the change
        console.log('Disabled parent node creation')
        // this.$set(node, "nodes", [newNode]);
      } else {
        this.editNodeId = node.id;
        this.edit = false
        this.$refs['edit-modal'].show()
      }
    },
  },
};
</script>

<style scoped>
</style>