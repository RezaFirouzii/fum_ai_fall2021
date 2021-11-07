import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class AStar {

    public static void search(State initialState) {

        var f_table = new HashMap<String, Integer>();
        var g_table = new HashMap<String, Integer>();

        var queue = new PriorityQueue<State>(Comparator.comparing(state -> f_table.get(state.hash())));
        var close = new PriorityQueue<State>(Comparator.comparing(state -> f_table.get(state.hash())));
        var visited = new HashSet<String>();

        f_table.put(initialState.hash(), heuristic(null, initialState));
        g_table.put(initialState.hash(), 0);

        queue.add(initialState);
        visited.add(initialState.hash());

        while (!visited.isEmpty()) {
            var current = queue.poll();

            if (isGoal(current)) {
                result(current);
                System.out.printf("Cost: %d\n", f_table.get(current.hash()));
                break;
            }

            var children = current.successor();
            for (var child: children) {
                int g = g_table.get(current.hash()) + 1;
                if (!visited.contains(child.hash())) {
                    g_table.put(child.hash(), g);
                    f_table.put(child.hash(), g + heuristic(current, child));
                    queue.add(child);
                    visited.add(child.hash());
                } else {
                    if (g < g_table.get(child.hash())) {
                        g_table.put(child.hash(), g);
                        f_table.put(child.hash(), g + heuristic(current, child));
                        if (close.contains(child)) {
                            close.remove(child);
                            queue.add(child);
                        }
                    }
                }
            }
            queue.remove(current);
            close.add(current);
        }
    }

    private static int heuristic(State parent, State current) {
        int h = 0;
        if (parent == null)
            parent = current;
        for (int i = 0; i < parent.getGraph().size(); i++)
            if (parent.getGraph().getNode(i).getColor() != Color.Green &&
                    current.getGraph().getNode(i).getColor() != Color.Green)
                h += 1;

        return h;
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
            FileWriter myWriter = new FileWriter("Astar_Result.txt");
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


