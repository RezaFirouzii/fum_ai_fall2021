import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class GBFS {

    public static void search(State initialState) {
        var costs = new HashMap<String, Integer>();
        var queue = new PriorityQueue<State>(Comparator.comparing(state -> costs.get(state.hash())));
        var visited = new HashSet<String>();

        costs.put(initialState.hash(), 0);
        queue.add(initialState);
        visited.add(initialState.hash());

        while (!queue.isEmpty()) {
            var current = queue.poll();
            if (isGoal(current)) {
                result(current);
                break;
            }
            var children = current.successor();
            for (var child: children) {
                if (!visited.contains(child.hash())) {
                    int child_cost = costs.get(current.hash()) + 1;
                    costs.put(child.hash(), child_cost);
                    queue.add(child);
                    visited.add(child.hash());
                }
            }
        }
    }

    private static boolean isGoal(State state){
        for (int i = 0; i < state.getGraph().size(); i++) {
            if(state.getGraph().getNode(i).getColor() == Color.Red
                    || state.getGraph().getNode(i).getColor() == Color.Black){
                return false;
            }
        }
        return true;
    }

    private static void result(State state){
        Stack<State>  states = new Stack<State>();
        while (true){
            states.push(state);
            if(state.getParentState() == null){
                break;
            }
            else {
                state = state.getParentState();
            }
        }
        try {
            FileWriter myWriter = new FileWriter("GBFS_Result.txt");
            System.out.println("initial state : ");
            while (!states.empty()){
                State tempState = states.pop();
                if(tempState.getSelectedNodeId() != -1) {
                    System.out.println("selected id : " + tempState.getSelectedNodeId());
                }
                tempState.getGraph().print();

                myWriter.write(tempState.getSelectedNodeId()+" ,");
                myWriter.write(tempState.outputGenerator()+"\n");
            }
            myWriter.close();
            System.out.println("Successfully wrote to the file.");
        } catch (IOException e) {
            System.out.println("An error occurred.");
            e.printStackTrace();
        }
    }
}


