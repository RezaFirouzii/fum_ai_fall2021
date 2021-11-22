import java.io.FileWriter;
import java.io.IOException;
import java.util.*;

public class UCS {

    private static class Entry {
        private int cost;
        private State state;

        Entry(int cost, State state) {
            this.cost = cost;
            this.state = state;
        }
    }

    public static void search(State initialState) {
        var answer = new Entry(Integer.MAX_VALUE, null);
        var queue = new PriorityQueue<Entry>(Comparator.comparingInt(entry -> entry.cost));
        var visited = new HashSet<String>();
        queue.add(new Entry(0, initialState));

        while (!queue.isEmpty()) {
            var current = queue.poll();
            if (isGoal(current.state) && answer.cost > current.cost)
                answer = current;
            if (!visited.contains(current.state.hash())) {
                var children = current.state.successor();
                for (var child: children)
                    queue.add(new Entry((current.cost + getCost(child)), child));
            }
            visited.add(current.state.hash());
        }
        result(answer);
    }

    private static int getCost(State child) {
        var parent = child.getParentState();
        var selectedNode = parent.getGraph().getNode(child.getSelectedNodeId());
        return switch (selectedNode.getColor()) {
            case Red -> 1;
            case Black -> 2;
            case Green -> 3;
        };
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

    private static void result(Entry answer){
        var state = answer.state;
        var minimumCost = answer.cost;
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
            FileWriter myWriter = new FileWriter("UCS_Result.txt");
            System.out.println("Minimum Cost : " + minimumCost);
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


