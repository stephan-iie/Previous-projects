<br>
    <a href = "/friendList"> Go back to friends list </a>
</br>

<ul id ="friendList">
    % for file in data:
      
      <li class="friend">
        <img src = "img/blankProfile.png"/>
        <div class ='Friend_name'>
         {{file}}
        </div>
      </li>
    % end
  </ul>